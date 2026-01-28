// Модальные окна
(function($) {
    "use strict";
    
    // Инициализация IMask
    function initMasks() {
        if (typeof IMask !== 'undefined') {
            IMask(document.getElementById('phone'), {
                mask: '+7 (000) 000 00 00'
            });
            
            IMask(document.getElementById('datepickerDefault'), {
                mask: '00.00.0000'
            });
            
            IMask(document.getElementById('f_time'), {
                mask: '00:00'
            });
        }
    }
    
    // Управление модальными окнами
    function initModals() {
        // Открытие/закрытие модалок
        $(document).on('click', '.modal-close, .modal-btn', function() {
            $(this).closest('.modal').fadeOut(300);
            $('body').css('overflow', '');
        });
        
        $(document).on('click', '.modal', function(e) {
            if (e.target === this) {
                $(this).fadeOut(300);
                $('body').css('overflow', '');
            }
        });
        
        // Открытие модалок по классу
        $(document).on('click', '.btn-order', function(e) {
            e.preventDefault();
            $('#callbackModal').fadeIn(300);
            $('body').css('overflow', 'hidden');
        });
        
        $(document).on('click', '.btn-question', function(e) {
            e.preventDefault();
            $('#questionModal').addClass('show');
        });
    }
    
    // Модалка успешной отправки
    function initSuccessModal() {
        $(document).on('submit', '#calculatorForm', function(e) {
            e.preventDefault();
            var form = $(this);
            var submitBtn = form.find('.submit-btn');
            
            submitBtn.prop('disabled', true).text('Отправляем...');
            
            $.ajax({
                url: form.attr('action') || window.submitFormUrl || '/submit/',
                type: 'POST',
                data: form.serialize(),
                headers: {
                    'X-CSRFToken': form.find('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if (response.success) {
                        $('#successMessage').text(response.message || 'Заявка успешно отправлена!');
                        $('#successModal')
                            .css('display', 'flex')
                            .hide()
                            .fadeIn(400);
                        
                        setTimeout(function() {
                            $('#successModal').fadeOut(300);
                        }, 5000);
                        
                        form[0].reset();
                    } else {
                        alert('Ошибка: ' + (response.message || 'Неизвестная ошибка'));
                    }
                },
                error: function(xhr) {
                    var errMsg = xhr.responseJSON ? xhr.responseJSON.message : 'Ошибка соединения';
                    alert('Ошибка: ' + errMsg);
                },
                complete: function() {
                    submitBtn.prop('disabled', false).text('ОФОРМИТЬ ЗАЯВКУ');
                }
            });
        });
    }
    
    // Инициализация при загрузке
    $(document).ready(function() {
        initMasks();
        initModals();
        initSuccessModal();
    });
    
})(jQuery);