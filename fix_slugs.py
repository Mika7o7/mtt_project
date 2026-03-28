from core.models import Page

# Словарь: (название для поиска, правильный slug)
fix_list = [
    # Метро
    ('АВИАМОТОРНАЯ', 'oblasti/evakuator-metro/evakuator-metro-aviamotornaya'),
    ('ВДНХ', 'oblasti/evakuator-metro/evakuator-vdnx'),
    ('БАБУШКИНСКАЯ', 'oblasti/evakuator-metro/evakuator-babushkinskaja'),
    
    # Города
    ('МОСКВА', 'oblasti/evakuator/evakuator-moskva'),
    ('КИТАЙ-ГОРОД', 'oblasti/evakuator/evakuator-v-kitaj-gorod'),
    ('КУНЦЕВО', 'oblasti/evakuator/evakuator-v-kunczevo'),
    
    # Шоссе
    ('ЯРОСЛАВСКОЕ ШОССЕ', 'oblasti/evakuatoryi-shosse/evakuator-v-yaroslavskoe-shosse'),
]

print("="*60)
print("ИСПРАВЛЕНИЕ SLUG")
print("="*60)

for search_name, correct_slug in fix_list:
    print(f"\n🔍 Ищем: ЭВАКУАТОР {search_name}")
    
    # Ищем страницу
    pages = Page.objects.filter(name__icontains=search_name)
    
    if pages.exists():
        page = pages.first()
        print(f"   Найдено: {page.name}")
        print(f"   Текущий slug: {page.slug}")
        print(f"   Новый slug: {correct_slug}")
        
        # Проверяем, не занят ли slug
        if Page.objects.filter(slug=correct_slug).exclude(id=page.id).exists():
            print(f"   ⚠ ОШИБКА: slug {correct_slug} уже занят!")
        else:
            page.slug = correct_slug
            page.save()
            print(f"   ✓ ИСПРАВЛЕНО!")
    else:
        print(f"   ❌ НЕ НАЙДЕНО: ЭВАКУАТОР {search_name}")

print("\n" + "="*60)
print("УДАЛЕНИЕ НЕПРАВИЛЬНЫХ СТРАНИЦ")
print("="*60)

# Удаляем страницы с английскими названиями
wrong_slugs = [
    'oblasti/evakuator-metro/evakuator-metro-aviamotornaya',
    'oblasti/evakuator-metro/evakuator-vdnx',
    'oblasti/evakuator-metro/evakuator-babushkinskaja',
    'oblasti/evakuator/evakuator-moskva',
    'oblasti/evakuator/evakuator-v-kitaj-gorod',
    'oblasti/evakuator/evakuator-v-kunczevo',
    'oblasti/evakuatoryi-shosse/evakuator-v-yaroslavskoe-shosse',
]

deleted = 0
for slug in wrong_slugs:
    try:
        page = Page.objects.get(slug=slug)
        print(f"\n🗑 Удаляем: {page.name} ({page.slug})")
        page.delete()
        deleted += 1
    except Page.DoesNotExist:
        print(f"\n⏭ Не найдено: {slug}")

print(f"\n✅ Удалено: {deleted}")

print("\n" + "="*60)
print("ПРОВЕРКА РЕЗУЛЬТАТА")
print("="*60)

for search_name, correct_slug in fix_list:
    try:
        page = Page.objects.get(slug=correct_slug)
        print(f"\n✅ {page.name}")
        print(f"   Slug: {page.slug}")
    except Page.DoesNotExist:
        print(f"\n❌ Не найдено: {correct_slug}")

print("\n✅ ГОТОВО!")