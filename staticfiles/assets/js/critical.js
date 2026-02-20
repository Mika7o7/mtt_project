// Критический код - загружается сразу
(function() {
    // 1. Cookie баннер
    document.addEventListener("DOMContentLoaded", function() {
        const banner = document.getElementById("cookieBanner");
        const acceptBtn = document.getElementById("cookieAccept");
        
        if (banner && acceptBtn && !localStorage.getItem("cookiesAccepted")) {
            setTimeout(() => banner.classList.add("show"), 1000);
            
            acceptBtn.addEventListener("click", function() {
                localStorage.setItem("cookiesAccepted", "true");
                banner.classList.remove("show");
                setTimeout(() => {
                    banner.style.display = "none";
                }, 500);
            });
        }
    });
    
    // 2. Минимальные маски для телефонов (fallback если IMask не загрузился)
    document.addEventListener('DOMContentLoaded', function() {
        if (window.$) {
            $('input[type="tel"]').on('input', function() {
                var value = $(this).val().replace(/\D/g, '');
                if (value.length > 0) {
                    if (!value.startsWith('7') && !value.startsWith('8')) {
                        value = '7' + value;
                    }
                    if (value.length > 1) {
                        var formatted = '+7 (' + value.substring(1, 4) + ') ' +
                                      value.substring(4, 7) + '-' +
                                      value.substring(7, 9) + '-' +
                                      value.substring(9, 11);
                        $(this).val(formatted.trim());
                    }
                }
            });
        }
    });
    
    // 3. Простейший бургер-меню для мобильных
    document.addEventListener('DOMContentLoaded', function() {
        const burger = document.getElementById("burger");
        const menu = document.getElementById("nav-menu");
        
        if (burger && menu) {
            burger.addEventListener("click", function() {
                burger.classList.toggle("active");
                menu.classList.toggle("active");
            });
        }
    });
})();