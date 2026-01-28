// Ленивая загрузка ресурсов
(function() {
    "use strict";
    
    function lazyLoad() {
        // Ленивая загрузка 3D модели
        if ('IntersectionObserver' in window && document.querySelector('.model-viewer-container')) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const script = document.createElement('script');
                        script.type = 'module';
                        script.src = 'https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js';
                        document.head.appendChild(script);
                        observer.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '200px' });
            
            const modelContainer = document.querySelector('.model-viewer-container');
            if (modelContainer) observer.observe(modelContainer);
        }
        
        // Ленивая загрузка IMask если не загрузился
        if (typeof IMask === 'undefined') {
            const script = document.createElement('script');
            script.src = 'https://unpkg.com/imask';
            script.defer = true;
            document.head.appendChild(script);
        }
    }
    
    // Запускаем после полной загрузки страницы
    window.addEventListener('load', function() {
        // Даем время на загрузку критичного контента
        setTimeout(lazyLoad, 2000);
    });
    
})();