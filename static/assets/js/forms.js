// Универсальная обработка всех AJAX-форм с reCAPTCHA v3
(function($) {
    "use strict";

    // Флаг инициализации reCAPTCHA
    var recaptchaReady = false;
    var recaptchaAction = 'submit';

    // Callback когда reCAPTCHA загружена
    window.recaptchaCallback = function() {
        recaptchaReady = true;
    };

    function initForms() {
        // Сохраняем исходный текст кнопок
        $('.ajax-form button[type="submit"]').each(function() {
            var $btn = $(this);
            if (!$btn.data('original-text')) {
                $btn.data('original-text', $btn.text());
            }
        });

        // Единый обработчик для всех форм с классом .ajax-form
        $(document).on('submit', '.ajax-form', async function(e) {
            e.preventDefault();
            var form = $(this);
            var message = form.find('.form-message');
            var btn = form.find('button[type="submit"]');
            var url = form.data('url') || '/universal_form/';
            var action = form.data('action') || 'submit';

            if (message.length) message.text('');
            if (btn.length) {
                btn.prop('disabled', true).text('Отправляем...');
            }

            var formData = new FormData(form[0]);

            try {
                // Получаем reCAPTCHA token
                var recaptchaToken = '';
                if (typeof grecaptcha !== 'undefined' && window.RECAPTCHA_SITE_KEY) {
                    try {
                        recaptchaToken = await grecaptcha.execute(window.RECAPTCHA_SITE_KEY, {action: action});
                        formData.set('g-recaptcha-response', recaptchaToken);
                    } catch (recaptchaError) {
                        console.warn('reCAPTCHA error:', recaptchaError);
                        if (message.length) {
                            message.css('color', '#f44336').text('Ошибка проверки reCAPTCHA. Попробуйте позже.');
                        }
                        if (btn.length) {
                            btn.prop('disabled', false).text(btn.data('original-text'));
                        }
                        return;
                    }
                }

                var response = await fetch(url, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
                    body: formData
                });

                var data = await response.json();

                if (response.ok && data.success) {
                    var successMsg = form.data('success') || 'Заявка отправлена! Мы перезвоним вам в ближайшее время.';
                    if (message.length) {
                        message.css('color', '#00c853').html(successMsg);
                    }
                    form[0].reset();
                } else {
                    throw new Error(data.message || 'Ошибка');
                }
            } catch (err) {
                if (message.length) {
                    message.css('color', '#f44336').text('Ошибка отправки. Попробуйте позже.');
                }
            } finally {
                if (btn.length) {
                    btn.prop('disabled', false);
                    btn.text(btn.data('original-text'));
                }
            }
        });
    }

    $(document).ready(function() {
        initForms();
    });

})(jQuery);
