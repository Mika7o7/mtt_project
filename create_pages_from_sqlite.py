# create_pages_from_sqlite.py
import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtt_project.settings')
django.setup()

from core.models import Page

# Пути к базам данных
BACKUP_DB = 'db.sqlite3_19.02.2026'
TARGET_DB = 'db.sqlite3'

def check_databases():
    """Проверяет наличие файлов баз данных"""
    if not os.path.exists(BACKUP_DB):
        print(f"❌ Файл бэкапа {BACKUP_DB} не найден!")
        return False
    
    print(f"📂 Бэкап БД: {BACKUP_DB} ({os.path.getsize(BACKUP_DB)} bytes)")
    print(f"📂 Целевая БД: {TARGET_DB}")
    return True

def get_data_from_backup():
    """Читает данные из бэкапа"""
    conn = sqlite3.connect(BACKUP_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {}
    
    tables = [
        ('core_city', 'city'),
        ('core_district', 'district'),
        ('core_region', 'region'),
        ('core_highway', 'highway'),
        ('core_gruzovoy', 'service_gruz'),
    ]
    
    for table_name, data_type in tables:
        try:
            cursor.execute(f"SELECT name, slug FROM {table_name}")
            rows = cursor.fetchall()
            data[data_type] = [{'name': row['name'], 'slug': row['slug']} for row in rows]
            print(f"   {table_name}: {len(rows)} записей")
        except sqlite3.OperationalError:
            print(f"   ⚠️ Таблица {table_name} не найдена в бэкапе")
            data[data_type] = []
    
    conn.close()
    return data

def create_or_update_page(item, page_type):
    """Создает или обновляет страницу"""
    
    name = item['name']
    slug = item['slug']
    
    # Формируем данные для страницы
    if page_type == 'city':
        page_name = f"Эвакуатор {name}"
        page_slug = slug if slug else f"evakuator-{name.lower().replace(' ', '-')}"
        meta_title = f"Эвакуатор {name} — быстро и недорого"
        meta_description = f"Вызов эвакуатора в городе {name}. Круглосуточно, низкие цены, срочная подача."
        meta_keywords = f"эвакуатор {name}, вызвать эвакуатор {name}, эвакуация {name} Круглосуточно, низкие цены, срочная подача."
        page_type_value = 'city'
        sub_description = f"Профессиональный эвакуатор в городе {name} 24/7"
        
    elif page_type == 'district':
        page_name = f"Эвакуатор {name}"
        page_slug = slug if slug else f"evakuator-{name.lower().replace(' ', '-')}"
        meta_title = f"Эвакуатор {name} — заказать в округе"
        meta_description = f"Эвакуатор в {name}. Быстрая подача, низкие цены, работаем круглосуточно."
        meta_keywords = f"эвакуатор {name}, эвакуация {name}, вызвать эвакуатор {name} Круглосуточно, низкие цены, срочная подача."
        page_type_value = 'district'
        sub_description = f"Профессиональный эвакуатор в округе {name} 24/7"
        
    elif page_type == 'region':
        page_name = f"Эвакуатор {name}"
        page_slug = slug if slug else f"evakuator-{name.lower().replace(' ', '-')}"
        meta_title = f"Эвакуатор {name} — услуги эвакуации"
        meta_description = f"Вызов эвакуатора в {name}. Круглосуточно, быстро, недорого."
        meta_keywords = f"эвакуатор {name}, эвакуация {name}, вызвать эвакуатор {name} Круглосуточно, низкие цены, срочная подача."
        page_type_value = 'region'
        sub_description = f"Профессиональный эвакуатор в регионе {name} 24/7"
        
    elif page_type == 'highway':
        page_name = f"Эвакуатор на {name}"
        page_slug = slug if slug else f"evakuator-na-{name.lower().replace(' ', '-')}"
        meta_title = f"Эвакуатор на {name} — быстро и недорого"
        meta_description = f"Вызов эвакуатора на {name}. Круглосуточно, оперативная подача, лучшие цены."
        meta_keywords = f"эвакуатор {name}, эвакуация {name}, вызвать эвакуатор {name} Круглосуточно, низкие цены, срочная подача."
        page_type_value = 'highway'
        sub_description = f"Профессиональный эвакуатор на шоссе {name} 24/7"
        
    elif page_type == 'service_gruz':
        # Убираем дублирование "ГРУЗОВОЙ ЭВАКУАТОР" в названии
        clean_name = name.replace('ГРУЗОВОЙ ЭВАКУАТОР', '').strip()
        if not clean_name:
            clean_name = name
        page_name = f"Грузовой эвакуатор {clean_name}"
        page_slug = slug if slug else f"gruzovoy-evakuator-{clean_name.lower().replace(' ', '-')}"
        meta_title = f"Грузовой эвакуатор {clean_name} в Москве"
        meta_description = f"Заказать грузовой эвакуатор {clean_name}. Перевозка спецтехники, автобусов, грузовиков."
        meta_keywords = f"грузовой эвакуатор {clean_name}, эвакуатор для грузовиков {clean_name}, эвакуация спецтехники Круглосуточно, низкие цены, срочная подача."
        page_type_value = 'service'
        sub_description = f"Профессиональный грузовой эвакуатор {clean_name} 24/7"
    
    else:
        return None, 'skipped'
    
    # Текст страницы (общий для всех)
    page_text = """Ищете, где можно вызвать эвакуатор по доступной цене? Наша компания предлагает оптимальное соотношение стоимости и качества услуг. Эвакуатор недорого — это реально, если обратиться к профессионалам с современным автопарком и отработанной системой работы. Стоимость эвакуатора в нашей компании одна из самых конкурентных на рынке. Мы понимаем, что ситуации на дороге бывают разными, и предлагаем гибкую систему ценообразования. Эвакуатор цена которого вас приятно удивит, будет у вас в течение 20 минут после звонка. Эвакуатор машин в нашей компании — это не просто транспортировка, а комплексное решение проблем. Мы работаем с автомобилями любой сложности. Эвакуатор круглосуточно — это наше основное преимущество. Мы понимаем, что проблемы на дороге не случаются по расписанию, поэтому работаем без выходных и перерывов. Наша служба поддержки принимает заказы 24/7. Не переплачивайте за качество! Наш эвакуатор дешево доставит ваш автомобиль в указанное место с максимальным комфортом и безопасностью."""
    
    # Проверяем, существует ли страница
    page, created = Page.objects.update_or_create(
        slug=page_slug,
        defaults={
            'page_type': page_type_value,
            'name': page_name,
            'info_name': page_name,
            'sub_description': sub_description,
            'page_title': "Услуги эвакуатора в Москве: оперативно, безопасно, круглосуточно",
            'page_text': page_text,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': meta_keywords,
            'fastorder': True,
            'calculator': True,
            'question_map': True,
            'map_show': True,
            'payment_show': True,
            'second_hero_section': True,
            'is_active': True,
            'order': 0
        }
    )
    
    return page, 'created' if created else 'updated'

def main():
    print("=" * 60)
    print("🚀 СОЗДАНИЕ/ОБНОВЛЕНИЕ СТРАНИЦ ИЗ БЭКАПА")
    print("=" * 60)
    
    # Проверяем базы данных
    if not check_databases():
        return
    
    # Читаем данные из бэкапа
    print("\n📊 Чтение данных из бэкапа:")
    data = get_data_from_backup()
    
    total_items = sum(len(items) for items in data.values())
    print(f"\n📊 Всего записей в бэкапе: {total_items}")
    
    # Спрашиваем подтверждение
    answer = input(f"\nСоздать/обновить страницы в текущей БД ({TARGET_DB})? (y/n): ")
    if answer.lower() != 'y':
        print("❌ Операция отменена")
        return
    
    print("\n🚀 Начинаем создание/обновление страниц...")
    
    stats = {
        'city': {'created': 0, 'updated': 0, 'skipped': 0},
        'district': {'created': 0, 'updated': 0, 'skipped': 0},
        'region': {'created': 0, 'updated': 0, 'skipped': 0},
        'highway': {'created': 0, 'updated': 0, 'skipped': 0},
        'service_gruz': {'created': 0, 'updated': 0, 'skipped': 0},
    }
    
    # Города
    print("\n📌 Города:")
    for item in data.get('city', []):
        page, status = create_or_update_page(item, 'city')
        if status == 'created':
            stats['city']['created'] += 1
            print(f"   ✅ Создана: {page.name}")
        elif status == 'updated':
            stats['city']['updated'] += 1
            print(f"   🔄 Обновлена: {page.name}")
    
    # Округа
    print("\n📌 Округа:")
    for item in data.get('district', []):
        page, status = create_or_update_page(item, 'district')
        if status == 'created':
            stats['district']['created'] += 1
            print(f"   ✅ Создана: {page.name}")
        elif status == 'updated':
            stats['district']['updated'] += 1
            print(f"   🔄 Обновлена: {page.name}")
    
    # Области
    print("\n📌 Области:")
    for item in data.get('region', []):
        page, status = create_or_update_page(item, 'region')
        if status == 'created':
            stats['region']['created'] += 1
            print(f"   ✅ Создана: {page.name}")
        elif status == 'updated':
            stats['region']['updated'] += 1
            print(f"   🔄 Обновлена: {page.name}")
    
    # Шоссе
    print("\n📌 Шоссе:")
    for item in data.get('highway', []):
        page, status = create_or_update_page(item, 'highway')
        if status == 'created':
            stats['highway']['created'] += 1
            print(f"   ✅ Создана: {page.name}")
        elif status == 'updated':
            stats['highway']['updated'] += 1
            print(f"   🔄 Обновлена: {page.name}")
    
    # Грузовые
    print("\n📌 Грузовые эвакуаторы:")
    for item in data.get('service_gruz', []):
        page, status = create_or_update_page(item, 'service_gruz')
        if status == 'created':
            stats['service_gruz']['created'] += 1
            print(f"   ✅ Создана: {page.name}")
        elif status == 'updated':
            stats['service_gruz']['updated'] += 1
            print(f"   🔄 Обновлена: {page.name}")
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГИ:")
    
    total_created = sum(s['created'] for s in stats.values())
    total_updated = sum(s['updated'] for s in stats.values())
    
    print(f"✅ Создано новых страниц: {total_created}")
    print(f"🔄 Обновлено существующих: {total_updated}")
    
    print("\n📊 По категориям:")
    for category, counts in stats.items():
        if counts['created'] > 0 or counts['updated'] > 0:
            print(f"   {category}: создано {counts['created']}, обновлено {counts['updated']}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()