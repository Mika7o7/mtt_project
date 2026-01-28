// Глобальная функция расчёта стоимости (доступна через window)
window.SumRez = function () {
    const vk = document.getElementById('clt_vk').value;
    const distanceInput = document.getElementById('f_qq');
    const distance = parseInt(distanceInput.value) || 0;
    let total = 0;

    if (distance <= 0) {
        document.querySelector('.clt_sum--js').textContent = '0';
        return;
    }

    const kolesoCount = parseInt(document.getElementById('clt_koleso')?.value) || 0;
    total += kolesoCount * 1500;

    let visibleSelect;
    let extrasContainer;

    if (vk === '1') {
        // Эвакуатор
        visibleSelect = document.querySelector('.clt_div_1--js .clt_tip--js:not(.hidden)');
        extrasContainer = document.querySelector('.clt_div_1--js .extras-grid:not(.hidden)');
    } else {
        // Манипулятор
        visibleSelect = document.querySelector('.clt_div_2--js .clt_tip--js:not(.hidden)');
        extrasContainer = document.querySelector('.clt_div_2--js .extras-grid:not(.hidden)');
    }

    if (visibleSelect) {
        const selectedOption = visibleSelect.selectedOptions[0];
        const basePrice = parseInt(selectedOption.dataset.price) || 0;
        const kmRate = parseInt(selectedOption.dataset.km) || 50;
        const kmPrice = distance * kmRate;

        total += basePrice + kmPrice;
    }

    // Дополнительные чекбоксы
    if (extrasContainer) {
        extrasContainer.querySelectorAll('input[type="checkbox"]:checked').forEach(cb => {
            total += parseInt(cb.dataset.price) || 0;
        });
    } else {
        // Fallback на старый селектор, если .extras-grid нет
        const divClass = (vk === '1') ? '.clt_div_1--js' : '.clt_div_2--js';
        document.querySelectorAll(`${divClass} input[type="checkbox"]:checked`).forEach(cb => {
            total += parseInt(cb.dataset.price) || 0;
        });
    }

    document.querySelector('.clt_sum--js').textContent = total.toLocaleString('ru-RU');
};

// =============================================
// Yandex Maps + роутинг
// =============================================
ymaps.ready(initMap);

function initMap() {
    const myMap = new ymaps.Map("map_map", {
        center: [55.755864, 37.617698],
        zoom: 9,
        controls: ["fullscreenControl"],
        behaviors: ["default", "scrollZoom", "drag"]
    });

    const routePanelControl = new ymaps.control.RoutePanel({
        options: {
            maxWidth: "280px",
            autofocus: false
        }
    });

    const zoomControl = new ymaps.control.ZoomControl({
        options: {
            size: "small",
            float: "none",
            position: { bottom: 45, right: 10 }
        }
    });

    const trafficControl = new ymaps.control.TrafficControl({
        state: {
            providerKey: "traffic#actual",
            trafficShown: true
        }
    });

    myMap.controls
        .add(trafficControl)
        .add(routePanelControl)
        .add(zoomControl);

    trafficControl.getProvider("traffic#actual").state.set("infoLayerShown", true);

    routePanelControl.routePanel.options.set({ types: { auto: true } });
    routePanelControl.routePanel.getRouteAsync().then(route => {
        route.model.setParams({ results: 1 }, true);

        route.model.events.add("requestsuccess", () => {
            const activeRoute = route.getActiveRoute();
            if (activeRoute) {
                const length = activeRoute.properties.get("distance");
                let qq = Math.round(length.value / 1000);
                if (qq < 1) qq = 1;

                document.getElementById('f_qq').value = qq;
                document.getElementById('f_qq').readOnly = true;
                SumRez();

                const wayPoints = route.model.getWayPoints();
                const addresses = wayPoints.map(p => p.properties.get("address"));
                const coordinates = wayPoints.map(p => p.properties.get("coordinates"));

                document.getElementById('f_mesto').value = addresses[0] || '';
                document.getElementById('f_end').value = addresses[1] || '';
                document.getElementById('f_mesto_cd').value = coordinates[0] || '';
                document.getElementById('f_end_cd').value = coordinates[1] || '';
            }
        });
    });

    // Отслеживание изменения точек маршрута
    routePanelControl.routePanel.state.events.add("change", () => {
        const fromValue = routePanelControl.routePanel.state.get("from");
        const toValue = routePanelControl.routePanel.state.get("to");

        const mesto = document.getElementById('f_mesto');
        const end = document.getElementById('f_end');
        const mestoCd = document.getElementById('f_mesto_cd');
        const endCd = document.getElementById('f_end_cd');
        const distInput = document.getElementById('f_qq');

        if (!fromValue) {
            mesto.value = '';
            mestoCd.value = '';
        } else {
            if (!toValue) {
                mesto.value = fromValue;
                mestoCd.value = '';
                end.value = '';
                endCd.value = '';
                distInput.readOnly = false;
            }
        }

        if (!toValue) {
            end.value = '';
            endCd.value = '';
            distInput.readOnly = false;
        }
    });
}

// =============================================
// DOMContentLoaded — основной код калькулятора
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded - initializing calculator');

    const vkInput = document.getElementById('clt_vk');
    const vidSelect = document.getElementById('clt_vid_1');
    const distanceInput = document.getElementById('f_qq');
    const sumElement = document.querySelector('.clt_sum--js');
    const kolesoLabel = document.querySelector('label[for="clt_koleso"]'); // Предполагаем, что лейбл существует

    function updateCategorySelect(isEvacuator) {
        const selectedVid = vidSelect.value;

        if (isEvacuator) {
            document.querySelectorAll('.clt_div_1--js .clt_tip--js').forEach(el => {
                el.classList.add('hidden');
            });
            const target = document.getElementById(`clt_tip_1_${selectedVid}`);
            if (target) target.classList.remove('hidden');
        } else {
            document.querySelectorAll('.clt_div_2--js .clt_tip--js').forEach(el => {
                el.classList.add('hidden');
            });
            const target = document.getElementById(`clt_tip_2_${selectedVid}`);
            if (target) target.classList.remove('hidden');
        }

        // Пересчитываем, если есть расстояние
        const dist = parseInt(distanceInput.value) || 0;
        if (dist > 0) {
            SumRez();
        } else {
            sumElement.textContent = '0';
        }
    }

    // Переключение Эвакуатор ↔ Манипулятор
    document.querySelectorAll('.switcher-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.switcher-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const vk = btn.dataset.vk;
            vkInput.value = vk;

            console.log('Switched to:', vk);

            // Скрываем оба блока
            document.querySelector('.clt_div_1--js')?.classList.add('hidden');
            document.querySelector('.clt_div_2--js')?.classList.add('hidden');

            if (vk === '1') {
                document.querySelector('.clt_div_1--js')?.classList.remove('hidden');
                if (kolesoLabel) kolesoLabel.textContent = 'Заблокированные колёса';
                updateCategorySelect(true);
            } else {
                document.querySelector('.clt_div_2--js')?.classList.remove('hidden');
                if (kolesoLabel) kolesoLabel.textContent = 'Отсутствующих колёс';
                updateCategorySelect(false);
            }

            SumRez();
        });
    });

    // Смена вида техники
    vidSelect.addEventListener('change', () => {
        console.log('Vid changed');
        const isEvac = vkInput.value === '1';
        updateCategorySelect(isEvac);
    });

    // Изначальная инициализация
    updateCategorySelect(true);

    // Пересчёт при изменении важных полей
    document.addEventListener('change', e => {
        const t = e.target;

        if (
            t.id === 'clt_vid_1' ||
            t.matches('.clt_tip--js') ||
            t.id === 'clt_koleso' ||
            t.id === 'f_qq' ||
            t.matches('.extra-checkbox input') ||
            t.type === 'checkbox'
        ) {
            SumRez();
        }
    });

    // Предзаказ — показ даты/времени
    const predzakaz = document.getElementById('clt_predzakaz');
    if (predzakaz) {
        predzakaz.addEventListener('change', () => {
            document.querySelector('.date-time-row')?.classList.toggle('hidden', !predzakaz.checked);
        });
    }

    // Доп. телефон
    const dphone = document.getElementById('clt_dphone');
    if (dphone) {
        dphone.addEventListener('change', () => {
            document.querySelector('.extra-contact-row')?.classList.toggle('hidden', !dphone.checked);
        });
    }

    // =============================================
    // Локальное сохранение состояния (кэш)
    // =============================================
    const CalculatorCache = {
        key: 'evac_calculator_state',
        ttl: 24 * 60 * 60 * 1000,

        save() {
            try {
                const state = {
                    timestamp: Date.now(),
                    data: {
                        vid: vidSelect.value,
                        vk: vkInput.value,
                        koleso: document.getElementById('clt_koleso')?.value,
                        distance: distanceInput.value,
                        name: document.querySelector('input[name="f_name"]')?.value || '',
                        phone: document.querySelector('input[name="f_phone"]')?.value || '',
                        comment: document.querySelector('textarea[name="f_ztxt"]')?.value || ''
                    }
                };
                localStorage.setItem(this.key, JSON.stringify(state));
            } catch (err) {
                console.warn('Cannot save to localStorage', err);
            }
        },

        load() {
            try {
                const saved = localStorage.getItem(this.key);
                if (!saved) return false;

                const state = JSON.parse(saved);
                if (Date.now() - state.timestamp >= this.ttl) {
                    localStorage.removeItem(this.key);
                    return false;
                }

                const d = state.data;
                if (d.vid) vidSelect.value = d.vid;
                if (d.vk) {
                    document.querySelectorAll('.switcher-btn').forEach(b => b.classList.remove('active'));
                    const btn = document.querySelector(`.switcher-btn[data-vk="${d.vk}"]`);
                    if (btn) btn.classList.add('active');
                    vkInput.value = d.vk;
                }
                if (d.koleso) document.getElementById('clt_koleso').value = d.koleso;
                if (d.distance && parseInt(d.distance) > 0) {
                    distanceInput.value = d.distance;
                }
                if (d.name) document.querySelector('input[name="f_name"]').value = d.name;
                if (d.phone) document.querySelector('input[name="f_phone"]').value = d.phone;
                if (d.comment) document.querySelector('textarea[name="f_ztxt"]').value = d.comment;

                return true;
            } catch (err) {
                console.warn('Cannot load from localStorage', err);
                return false;
            }
        },

        clear() {
            try {
                localStorage.removeItem(this.key);
            } catch (err) {
                console.warn('Cannot clear localStorage', err);
            }
        }
    };

    // Автосохранение при изменении полей
    const saveFields = '#clt_vid_1, #clt_koleso, #f_qq, input[name="f_name"], input[name="f_phone"], textarea[name="f_ztxt"], .clt_tip--js, input[type="checkbox"]';
    document.addEventListener('change', e => {
        if (e.target.matches(saveFields)) {
            setTimeout(() => CalculatorCache.save(), 120);
        }
    });
    document.addEventListener('input', e => {
        if (e.target.matches('input[name="f_name"], input[name="f_phone"], textarea[name="f_ztxt"]')) {
            setTimeout(() => CalculatorCache.save(), 120);
        }
    });

    // Восстановление при загрузке
    window.addEventListener('load', () => {
        setTimeout(() => {
            if (CalculatorCache.load()) {
                console.log('Calculator state restored from cache');
                const isEvac = vkInput.value === '1';
                updateCategorySelect(isEvac);

                const dist = parseInt(distanceInput.value) || 0;
                if (dist > 0) SumRez();
            }
        }, 500);
    });

    // Очистка кэша после отправки формы
    const form = document.getElementById('calculatorForm');
    if (form) {
        form.addEventListener('submit', () => {
            CalculatorCache.clear();
        });
    }

    console.log('Calculator initialized successfully');
});