// Обработка всех форм
(function($) {
    "use strict";
    
    function initForms() {
        // Обработка формы обратного звонка
        $('#callbackForm').on('submit', async function(e) {
            e.preventDefault();
            var form = $(this);
            var message = $('#formMessage');
            var submitBtn = form.find('button[type="submit"]');
            
            message.text('');
            submitBtn.prop('disabled', true).text('Отправляем...');
            
            try {
                var formData = new FormData(form[0]);
                var response = await fetch(window.callbackUrl || '/send_callback/', {
                    method: "POST",
                    headers: { "X-CSRFToken": formData.get('csrfmiddlewaretoken') },
                    body: formData,
                });
                
                if (response.ok) {
                    message.css('color', 'green').text('✅ Заявка успешно отправлена!');
                    form[0].reset();
                } else {
                    throw new Error();
                }
            } catch (error) {
                message.css('color', 'red').text('❌ Ошибка при отправке. Попробуйте позже.');
            } finally {
                submitBtn.prop('disabled', false).text('Отправить');
            }
        });
        
        // Обработка формы вопроса
        $('#questionForm').on('submit', async function(e) {
            e.preventDefault();
            var form = $(this);
            var message = $('#questionMessage');
            
            message.text('Отправка...');
            
            try {
                var formData = new FormData(form[0]);
                var response = await fetch('/send_callback_question/', {
                    method: "POST",
                    body: formData,
                });
                
                var data = await response.json();
                message.text(data.message);
                message.css('color', data.success ? "#28a745" : "#e63946");
                if (data.success) form[0].reset();
            } catch (error) {
                message.text('Ошибка отправки. Попробуйте позже.');
                message.css('color', "#e63946");
            }
        });
        
        // Обработка всех форм с классом .universal-form
        $('.universal-form').on('submit', async function(e) {
            e.preventDefault();
            var form = $(this);
            var message = form.find('.form-message');
            var btn = form.find('button[type="submit"]');
            
            if (message.length) message.text('');
            if (btn.length) {
                btn.prop('disabled', true);
                btn.text('Отправляем...');
            }
            
            try {
                var formData = new FormData(form[0]);
                formData.set('agree_policy', 'true');
                
                var response = await fetch(window.callbackUrl || '/send_callback/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
                    body: formData
                });
                
                var data = await response.json();
                
                if (response.ok && data.success) {
                    if (message.length) {
                        message.css('color', '#00c853');
                        message.html('Заявка отправлена!<br>Мы перезвоним вам в ближайшее время');
                    }
                    form[0].reset();
                } else {
                    throw new Error(data.message || 'Ошибка');
                }
            } catch (err) {
                if (message.length) {
                    message.css('color', '#f44336');
                    message.text('Ошибка отправки. Попробуйте позже.');
                }
            } finally {
                if (btn.length) {
                    btn.prop('disabled', false);
                    btn.text('Заказать эвакуатор');
                }
            }
        });
    }
    
    // Инициализация при загрузке
    $(document).ready(function() {
        initForms();
    });
    
})(jQuery);