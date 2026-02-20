// Меню и навигация
(function() {
    "use strict";
    
    function initMenu() {
        // Мега-меню
        const megaMenu = document.getElementById('mega-menu');
        const burgerx = document.getElementById('burger');
        const dropdownToggle = document.getElementById('services-toggle');
        
        if (dropdownToggle && megaMenu) {
            dropdownToggle.addEventListener('click', function(e) {
                e.stopPropagation();
                megaMenu.classList.toggle('active');
                if (burgerx) burgerx.style.display = "none";
            });
            
            megaMenu.addEventListener('click', function(e) {
                if (e.target === megaMenu) {
                    megaMenu.classList.remove('active');
                    if (burgerx) burgerx.style.display = "flex";
                }
            });
        }
        
        // Бургер меню с панелями
        const burger = document.getElementById("burger");
        const menu = document.getElementById("nav-menu");
        const sidePanels = document.querySelector(".sbp-side-panels");
        
        if (burger && menu && sidePanels) {
            burger.addEventListener("click", function() {
                burger.classList.toggle("active");
                menu.classList.toggle("active");
                
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
            
            // Закрытие меню по клику на ссылку
            document.querySelectorAll("#nav-menu a").forEach(link => {
                link.addEventListener("click", function() {
                    burger.classList.remove("active");
                    menu.classList.remove("active");
                    
                    if (window.innerWidth <= 768) {
                        sidePanels.style.opacity = "1";
                        sidePanels.style.visibility = "visible";
                        sidePanels.style.pointerEvents = "auto";
                    }
                });
            });
            
            // Сброс стилей при ресайзе
            window.addEventListener("resize", function() {
                if (window.innerWidth > 768) {
                    sidePanels.style.cssText = "";
                }
            });
        }
        
        // FAQ аккордеон
        document.querySelectorAll(".faq-question").forEach(question => {
            question.addEventListener("click", function() {
                const item = question.closest(".faq-item");
                item.classList.toggle("active");
            });
        });
        
        // Fake select
        document.querySelectorAll('.fake-select').forEach(select => {
            const title = select.querySelector('.fake-select__title');
            if (title) {
                title.addEventListener('click', function(e) {
                    e.stopPropagation();
                    document.querySelectorAll('.fake-select').forEach(s => {
                        if (s !== select) s.classList.remove('active');
                    });
                    select.classList.toggle('active');
                });
            }
        });
        
        // Закрытие fake-select при клике вне
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.fake-select') && !e.target.closest('#services-toggle')) {
                document.querySelectorAll('.fake-select').forEach(s => {
                    s.classList.remove('active');
                });
            }
        });
    }
    
    // Инициализация при загрузке
    document.addEventListener('DOMContentLoaded', initMenu);
    
})();