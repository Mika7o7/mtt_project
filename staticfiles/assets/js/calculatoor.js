// static/assets/js/calculator.js — УНИВЕРСАЛЬНЫЙ 2025 (работает на всех сайтах эвакуаторов)
document.addEventListener("DOMContentLoaded", () => {
  console.log("Инициализация калькулятора v2.1 — УНИВЕРСАЛЬНАЯ ВЕРСИЯ");

  // Ищем поле расстояния по всем возможным вариантам
  const distanceField = document.querySelector(".clt_km--js") ||
                        document.querySelector(".clt_km_js") ||
                        document.querySelector("#f_qq") ||
                        document.querySelector("input[name='f_qq']") ||
                        document.querySelector("input[name='distance']") ||
                        document.querySelector("input[name='distance_km']") ||
                        document.querySelector(".distance-input");

  // Ищем поле цены
  const priceField = document.querySelector(".clt_sum--js") ||
                     document.querySelector(".clt_sum_js") ||
                     document.querySelector(".total-price") ||
                     document.querySelector("#total_price") ||
                     document.querySelector(".price-total");

  // Если не нашли — ругаемся в консоль (чтобы ты точно увидел)
  if (!distanceField) console.error("ПОЛЕ РАССТОЯНИЯ НЕ НАЙДЕНО! Добавь класс clt_km--js или id='f_qq'");
  if (!priceField)    console.error("ПОЛЕ ЦЕНЫ НЕ НАЙДЕНО! Добавь класс clt_sum--js");

  const mapContainer = document.getElementById("map_map");
  if (!mapContainer) {
    console.warn("Контейнер #map_map не найден");
    return;
  }

  // Ждём Яндекс.Карты
  function waitForYmaps() {
    if (typeof ymaps !== "undefined" && ymaps.ready) {
      ymaps.ready(initMap);
    } else {
      setTimeout(waitForYmaps, 200);
    }
  }
  waitForYmaps();

  function initMap() {
    console.log("Яндекс.Карты v2.1 загружены — запускаем!");

    const map = new ymaps.Map("map_map", {
      center: [55.751574, 37.573856],
      zoom: 10,
      controls: []
    });

    const routePanel = new ymaps.control.RoutePanel({
      options: {
        maxWidth: "360px",
        showHeader: false,
        autofocus: true
      }
    });

    // ТОЛЬКО АДРЕСА — НИКАКИХ КООРДИНАТ
    routePanel.routePanel.options.set({
      types: { auto: true },
      reverseGeocoding: true,
      allowSwitch: false
    });

    map.controls.add(routePanel);

    routePanel.routePanel.getRouteAsync().then(route => {
      route.model.events.add("requestsuccess", () => {
        const activeRoute = route.getActiveRoute();

        if (!activeRoute) {
          if (distanceField) distanceField.value = "";
          if (priceField) priceField.textContent = "0 ₽";
          if (typeof SumRez === "function") SumRez();
          return;
        }

        const distanceMeters = activeRoute.properties.get("distance").value;
        const km = Math.max(1, Math.round(distanceMeters / 1000));

        if (distanceField) distanceField.value = km;
        if (priceField) {
          let price = 3000;
          if (km > 10) price += (km - 10) * 300;
          priceField.textContent = price.toLocaleString("ru-RU") + " ₽";
        }

        if (typeof SumRez === "function") SumRez();
      });
    });
  }
});