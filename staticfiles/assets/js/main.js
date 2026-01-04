document.addEventListener('DOMContentLoaded', () => {
  const megaMenu = document.getElementById('mega-menu');
  const burgerx = document.getElementById('burger');
  const dropdownToggle = document.getElementById('services-toggle');

  // Открытие меню
  dropdownToggle.addEventListener('click', () => {
    megaMenu.classList.toggle('active');
    burgerx.style.display = "none";

  });

  // Закрытие при клике на фон
  megaMenu.addEventListener('click', (e) => {
    // Если кликнули именно по фону, а не по контейнеру внутри
    if (e.target === megaMenu) {
      megaMenu.classList.remove('active');
      burgerx.style.display = "flex";
    }
  });
});




document.addEventListener("DOMContentLoaded", () => {
    const burger     = document.getElementById("burger");
    const menu       = document.getElementById("nav-menu");
    const sidePanels = document.querySelector(".sbp-side-panels"); // правильно!

    if (!burger || !menu || !sidePanels) return; // защита от ошибок

    // Открытие/закрытие бургера
    burger.addEventListener("click", () => {
        burger.classList.toggle("active");
        menu.classList.toggle("active");

        // Скрываем/показываем боковые панели только на телефоне
        if (window.innerWidth <= 768) {
            if (menu.classList.contains("active")) {
                sidePanels.style.opacity = "0";
                sidePanels.style.visibility = "hidden";
                sidePanels.style.pointerEvents = "none";
            } else {
                sidePanels.style.opacity = "1";
                sidePanels.style.visibility = "visible";
                sidePanels.style.pointerEvents = "auto";
            }
        }
    });

    // Закрытие меню по клику на ссылку (мобильная версия)
    document.querySelectorAll("#nav-menu a").forEach(link => {
        link.addEventListener("click", () => {
            burger.classList.remove("active");
            menu.classList.remove("active");

            // Возвращаем панели при закрытии меню
            if (window.innerWidth <= 768) {
                sidePanels.style.opacity = "1";
                sidePanels.style.visibility = "visible";
                sidePanels.style.pointerEvents = "auto";
            }
        });
    });

    // На всякий случай — при изменении размера окна
    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            sidePanels.style.cssText = ""; // сбрасываем стили на десктопе
        }
    });
});
        // Модального окна Заказать звонок
        document.addEventListener("DOMContentLoaded", () => {
          const modal = document.getElementById("callbackModal");
          const openBtns = document.querySelectorAll(".btn-order"); // на случай, если их несколько
          const closeBtn = document.querySelector(".modal-close");
          const form = document.getElementById("callbackForm");
          const message = document.getElementById("formMessage");
        
          openBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
              e.preventDefault();
              modal.style.display = "flex";
              document.body.style.overflow = "hidden";
            });
          });
      
          closeBtn.addEventListener("click", () => {
            modal.style.display = "none";
            document.body.style.overflow = "";
            message.textContent = "";
          });
      
          window.addEventListener("click", (e) => {
            if (e.target === modal) {
              modal.style.display = "none";
              document.body.style.overflow = "";
              message.textContent = "";
            }
          });
      
          form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
        
            try {
              const response = await fetch("{% url 'send_callback' %}", {
                method: "POST",
                headers: { "X-CSRFToken": formData.get('csrfmiddlewaretoken') },
                body: formData,
              });
          
              if (response.ok) {
                message.style.color = "green";
                message.textContent = "✅ Заявка успешно отправлена!";
                form.reset();
              } else {
                throw new Error();
              }
            } catch (error) {
              message.style.color = "red";
              message.textContent = "❌ Ошибка при отправке. Попробуйте позже.";
            }
          });
        });
        // Модального окна вопрос
        document.addEventListener("DOMContentLoaded", () => {
          const questionModal = document.getElementById("questionModal");
          const openQuestionBtn = document.querySelector('.btn-question');
          const closeQuestionBtn = questionModal.querySelector('.modal-close');
          const questionForm = document.getElementById("questionForm");
          const questionMessage = document.getElementById("questionMessage");

          if (!openQuestionBtn) {
            console.warn("Кнопка .btn-question не найдена");
            return;
          }
      
          openQuestionBtn.addEventListener("click", (e) => {
            e.preventDefault();
            questionModal.classList.add("show");
          });
      
          closeQuestionBtn.addEventListener("click", () => {
            questionModal.classList.remove("show");
          });
      
          window.addEventListener("click", (e) => {
            if (e.target === questionModal) {
              questionModal.classList.remove("show");
            }
          });
      
          questionForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            questionMessage.textContent = "Отправка...";
            const formData = new FormData(questionForm);
        
            try {
              const response = await fetch("/send_callback_question/", {
                method: "POST",
                body: formData,
              });
              const data = await response.json();
              questionMessage.textContent = data.message;
              questionMessage.style.color = data.success ? "#28a745" : "#e63946";
              if (data.success) questionForm.reset();
            } catch (error) {
              questionMessage.textContent = "Ошибка отправки. Попробуйте позже.";
              questionMessage.style.color = "#e63946";
            }
          });
        });

        // faq-question
        document.querySelectorAll(".faq-question").forEach(question => {
            question.addEventListener("click", () => {
                const item = question.closest(".faq-item");
                item.classList.toggle("active");
            });
        });

        document.addEventListener('DOMContentLoaded', function () {

    // Находим ВСЕ формы с классом .contact-form (или любой другой класс, который ты используешь)
    document.querySelectorAll('.contact-form').forEach(form => {

        const messageDiv = form.querySelector('.form-message'); // место для ответа
        const submitBtn  = form.querySelector('button[type="submit"]');

        // При отправке формы
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Очищаем старое сообщение и блокируем кнопку
            if (messageDiv) messageDiv.textContent = '';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Отправляем...';
            }

            const formData = new FormData(form);

            try {
                const response = await fetch("{% url 'send_callback' %}", {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    },
                    body: formData
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    if (messageDiv) {
                        messageDiv.style.color = '#00c853';
                        messageDiv.textContent = result.message || 'Заявка успешно отправлена!';
                    }
                    form.reset();
                } else {
                    throw new Error(result.message || 'Ошибка');
                }

            } catch (err) {
                if (messageDiv) {
                    messageDiv.style.color = '#f44336';
                    messageDiv.textContent = err.message || 'Ошибка при отправке. Попробуйте позже.';
                }
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Отправить';
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {

   
    // Обработка ВСЕХ форм с классом .universal-form
    document.querySelectorAll('.universal-form').forEach(form => {
        const message = form.querySelector('.form-message');
        const btn     = form.querySelector('button[type="submit"]');

        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Очистка
            if (message) message.textContent = '';
            if (btn) {
                btn.disabled = true;
                btn.textContent = 'Отправляем...';
            }

            const formData = new FormData(form);

            // Принудительно отправляем согласие = true (даже если чекбокс disabled)
            formData.set('agree_policy', 'true');

            try {
                const resp = await fetch("{% url 'send_callback' %}", {
                    method: 'POST',
                    headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
                    body: formData
                });

                const data = await resp.json();

                if (resp.ok && data.success) {
                    if (message) {
                        message.style.color = '#00c853';
                        message.innerHTML = 'Заявка отправлена!<br>Мы перезвоним вам в ближайшее время';
                    }
                    form.reset();
                } else {
                    throw new Error(data.message || 'Ошибка');
                }
            } catch (err) {
                if (message) {
                    message.style.color = '#f44336';
                    message.textContent = 'Ошибка отправки. Попробуйте позже.';
                }
            } finally {
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = 'Заказать эвакуатор';
                }
            }
        });
    });
});


       
        
        

        document.querySelectorAll('.fake-select').forEach(select => {
    const title = select.querySelector('.fake-select__title');
    title.addEventListener('click', () => {
        // Закрываем все остальные
        document.querySelectorAll('.fake-select').forEach(s => {
            if (s !== select) s.classList.remove('active');
        });
        // Переключаем текущий
        select.classList.toggle('active');
    });
});

// Закрываем при клике вне
document.addEventListener('click', (e) => {
    if (!e.target.closest('.fake-select') && !e.target.closest('#services-toggle')) {
        document.querySelectorAll('.fake-select').forEach(s => s.classList.remove('active'));
    }
});