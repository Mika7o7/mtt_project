# create_pages.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtt_project.settings')  # замените на ваше название
django.setup()

from core.models import (
    MetroStation, Gruzovoy, Manipulyator, Highway, 
    District, Region, City, TransportType, Page
)

# База для копирования (Эвакуатор Зеленоград)
SOURCE_PAGE_SLUG = 'evakuator-zelenograd'  # замените на реальный slug страницы-образца

def get_source_page():
    """Получает страницу-образец для копирования настроек"""
    try:
        return Page.objects.get(slug=SOURCE_PAGE_SLUG)
    except Page.DoesNotExist:
        print(f"Страница-образец с slug '{SOURCE_PAGE_SLUG}' не найдена!")
        return None

def create_page_from_object(obj, page_type, source_page):
    """Создает страницу на основе объекта и страницы-образца"""
    
    # Определяем название в зависимости от типа
    if page_type == 'metro':
        name = f"Эвакуатор {obj.name}"
        slug = f"evakuator-{obj.slug}" if obj.slug else f"evakuator-{obj.name.lower().replace(' ', '-')}"
        h1 = f"Эвакуатор {obj.name}"
        meta_title = f"Эвакуатор {obj.name} — быстро и недорого"
        meta_description = f"Вызов эвакуатора в районе {obj.name}. Круглосуточно, низкие цены, срочная подача. Закажите эвакуатор прямо сейчас!"
        meta_keywords = f"эвакуатор {obj.name}, вызов эвакуатора {obj.name}, эвакуатор недорого {obj.name}"
        
    elif page_type == 'service' and hasattr(obj, 'name'):
        if isinstance(obj, Gruzovoy):
            name = f"Грузовой эвакуатор {obj.name}"
            slug = f"gruzovoy-{obj.slug}"
            h1 = f"Грузовой эвакуатор {obj.name}"
            meta_title = f"Грузовой эвакуатор {obj.name} в Москве"
            meta_description = f"Заказать грузовой эвакуатор {obj.name}. Перевозка спецтехники, автобусов, грузовиков. Работаем круглосуточно."
            meta_keywords = f"грузовой эвакуатор {obj.name}, эвакуатор для грузовиков {obj.name}, эвакуация спецтехники"
            
        elif isinstance(obj, Manipulyator):
            name = f"Эвакуатор-манипулятор {obj.name}"
            slug = f"manipulyator-{obj.slug}"
            h1 = f"Эвакуатор с манипулятором {obj.name}"
            meta_title = f"Эвакуатор-манипулятор {obj.name} — заказать"
            meta_description = f"Эвакуатор с краном-манипулятором {obj.name}. Погрузка и перевозка любой техники. Низкие цены, выезд 24/7."
            meta_keywords = f"эвакуатор манипулятор {obj.name}, кран манипулятор {obj.name}, эвакуатор с краном"
            
        elif isinstance(obj, Highway):
            name = f"Эвакуатор на {obj.name}"
            slug = f"{obj.slug}"
            h1 = f"Эвакуатор на {obj.name}"
            meta_title = f"Эвакуатор на {obj.name} — быстро и недорого"
            meta_description = f"Вызов эвакуатора на {obj.name}. Круглосуточно, оперативная подача, лучшие цены. Звоните!"
            meta_keywords = f"эвакуатор {obj.name}, вызвать эвакуатор {obj.name}, эвакуация {obj.name}"
            
        elif isinstance(obj, District):
            name = f"Эвакуатор {obj.name}"
            slug = f"{obj.slug}"
            h1 = f"Эвакуатор {obj.name}"
            meta_title = f"Эвакуатор {obj.name} — заказать в округе"
            meta_description = f"Эвакуатор в {obj.name}. Быстрая подача, низкие цены, работаем круглосуточно. Закажите прямо сейчас!"
            meta_keywords = f"эвакуатор {obj.name}, эвакуация {obj.name}, вызвать эвакуатор {obj.name}"
            
        elif isinstance(obj, Region):
            name = f"Эвакуатор {obj.name}"
            slug = f"{obj.slug}"
            h1 = f"Эвакуатор в {obj.name}"
            meta_title = f"Эвакуатор в {obj.name} — услуги эвакуации"
            meta_description = f"Вызов эвакуатора в {obj.name}. Круглосуточно, быстро, недорого. Работаем по всей области."
            meta_keywords = f"эвакуатор {obj.name}, эвакуация {obj.name}, вызвать эвакуатор {obj.name}"
            
        elif isinstance(obj, City):
            name = f"Эвакуатор {obj.name}"
            slug = f"{obj.slug}"
            h1 = f"Эвакуатор {obj.name}"
            meta_title = f"Эвакуатор {obj.name} — быстро и недорого"
            meta_description = f"Вызов эвакуатора в {obj.name}. Круглосуточно, оперативная подача, лучшие цены. Звоните!"
            meta_keywords = f"эвакуатор {obj.name}, вызвать эвакуатор {obj.name}, эвакуация {obj.name}"
            
        elif isinstance(obj, TransportType):
            name = f"Эвакуатор {obj.name}"
            slug = f"{obj.slug}"
            h1 = f"Эвакуатор {obj.name}"
            meta_title = f"Эвакуатор {obj.name} — заказать"
            meta_description = f"Заказать эвакуатор {obj.name}. Профессиональная эвакуация, низкие цены, работаем круглосуточно."
            meta_keywords = f"эвакуатор {obj.name}, эвакуация {obj.name}, вызвать эвакуатор {obj.name}"
    
    else:
        return None

    # Проверяем, не существует ли уже такая страница
    if Page.objects.filter(slug=slug).exists():
        print(f"⚠ Страница с slug '{slug}' уже существует. Пропускаем.")
        return None

    # Создаем страницу
    page = Page(
        page_type=page_type,
        name=name,
        slug=slug,
        info_name=h1,
        sub_description=source_page.sub_description,
        page_title=source_page.page_title,
        page_text=source_page.page_text,
        meta_title=meta_title,
        meta_description=meta_description,
        meta_keywords=meta_keywords,
        fastorder=source_page.fastorder,
        calculator=source_page.calculator,
        question_map=source_page.question_map,
        map_show=source_page.map_show,
        payment_show=source_page.payment_show,
        second_hero_section=source_page.second_hero_section,
        is_active=True,
        order=0,
    )
    page.save()
    
    # Копируем ManyToMany связи
    if source_page.hero_sections.exists():
        page.hero_sections.set(source_page.hero_sections.all())
    
    if source_page.how_to_order_steps.exists():
        page.how_to_order_steps.set(source_page.how_to_order_steps.all())
    
    if source_page.transport_types.exists():
        page.transport_types.set(source_page.transport_types.all())
    
    if source_page.why_choose_us.exists():
        page.why_choose_us.set(source_page.why_choose_us.all())
    
    if source_page.info_sections.exists():
        page.info_sections.set(source_page.info_sections.all())
    
    if source_page.price_items.exists():
        page.price_items.set(source_page.price_items.all())
    
    if source_page.work_photos.exists():
        page.work_photos.set(source_page.work_photos.all())
    
    if source_page.faqs.exists():
        page.faqs.set(source_page.faqs.all())
    
    if source_page.ratings.exists():
        page.ratings.set(source_page.ratings.all())
    
    if source_page.articles.exists():
        page.articles.set(source_page.articles.all())
    
    # Добавляем сам объект в соответствующее поле
    if page_type == 'metro':
        page.metro_stations.add(obj)
    elif page_type == 'service':
        if isinstance(obj, Gruzovoy):
            page.gruzovoys.add(obj)
        elif isinstance(obj, Manipulyator):
            page.manipulyators.add(obj)
        elif isinstance(obj, Highway):
            page.highways.add(obj)
        elif isinstance(obj, District):
            page.districts.add(obj)
        elif isinstance(obj, Region):
            page.regions.add(obj)
        elif isinstance(obj, City):
            page.cities.add(obj)
        elif isinstance(obj, TransportType):
            page.transport_types.add(obj)
    
    print(f"✅ Создана страница: {name} (slug: {slug})")
    return page


def main():
    source_page = get_source_page()
    if not source_page:
        return
    
    print("=" * 60)
    print("НАЧИНАЕМ СОЗДАНИЕ СТРАНИЦ")
    print("=" * 60)
    
    # 1. Метро
    print("\n📌 СОЗДАНИЕ СТРАНИЦ МЕТРО:")
    metro_stations = MetroStation.objects.all()
    for metro in metro_stations:
        create_page_from_object(metro, 'metro', source_page)
    
    # 2. Грузовые эвакуаторы
    print("\n📌 СОЗДАНИЕ СТРАНИЦ ГРУЗОВЫХ ЭВАКУАТОРОВ:")
    gruzovoys = Gruzovoy.objects.all()
    for gruz in gruzovoys:
        create_page_from_object(gruz, 'service', source_page)
    
    # 3. Манипуляторы
    print("\n📌 СОЗДАНИЕ СТРАНИЦ МАНИПУЛЯТОРОВ:")
    manipulyators = Manipulyator.objects.all()
    for manip in manipulyators:
        create_page_from_object(manip, 'service', source_page)
    
    # 4. Шоссе
    print("\n📌 СОЗДАНИЕ СТРАНИЦ ШОССЕ:")
    highways = Highway.objects.all()
    for highway in highways:
        create_page_from_object(highway, 'service', source_page)
    
    # 5. Округа
    print("\n📌 СОЗДАНИЕ СТРАНИЦ ОКРУГОВ:")
    districts = District.objects.all()
    for district in districts:
        create_page_from_object(district, 'service', source_page)
    
    # 6. Области
    print("\n📌 СОЗДАНИЕ СТРАНИЦ ОБЛАСТЕЙ:")
    regions = Region.objects.all()
    for region in regions:
        create_page_from_object(region, 'service', source_page)
    
    # 7. Города МО
    print("\n📌 СОЗДАНИЕ СТРАНИЦ ГОРОДОВ МО:")
    cities = City.objects.all()
    for city in cities:
        create_page_from_object(city, 'service', source_page)
    
    # 8. Типы транспорта
    print("\n📌 СОЗДАНИЕ СТРАНИЦ ТИПОВ ТРАНСПОРТА:")
    transport_types = TransportType.objects.all()
    for transport in transport_types:
        create_page_from_object(transport, 'service', source_page)
    
    print("\n" + "=" * 60)
    print("✅ СОЗДАНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)


if __name__ == "__main__":
    main()