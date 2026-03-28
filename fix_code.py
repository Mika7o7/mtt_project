#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('/home/mika/Desktop/projects/mtt_project')

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtt_project.settings')

# Инициализируем Django
django.setup()

import re
from django.utils.text import slugify
from core.models import Page

# Словарь для перевода названий городов с латиницы на русский
LATIN_TO_RUSSIAN = {
    'balashixa': 'Балашиха',
    'vidnoe': 'Видное',
    'dzerzhinskiy': 'Дзержинский',
    'korolev': 'Королев',
    'dmitrov': 'Дмитров',
    'dolgoprudnyij': 'Долгопрудный',
    'zheleznodorozhnyij': 'Железнодорожный',
    'ivanteevka': 'Ивантеевка',
    'klin': 'Клин',
    'krasnoarmejsk': 'Красноармейск',
    'krasnogorsk': 'Красногорск',
    'lobnya': 'Лобня',
    'lyitkarino': 'Лыткарино',
    'myitishhi': 'Мытищи',
    'odinczovo': 'Одинцово',
    'podolsk': 'Подольск',
    'reutov': 'Реутов',
    'sergiev-posad': 'Сергиев Посад',
    'solnechnogorsk': 'Солнечногорск',
    'sofrino': 'Софрино',
    'fryazino': 'Фрязино',
    'ximki': 'Химки',
    'shhelkovo': 'Щелково',
    'shherbinka': 'Щербинка',
    'elektrostal': 'Электросталь',
    'noginsk': 'Ногинск',
    'pushkino': 'Пушкино',
    'ramenskoe': 'Раменское',
    'domodedovo': 'Домодедово',
    'moskva': 'Москва',
    'moskovskaya-oblast': 'Московская область',
    'novoryazanskoe-shosse': 'Новорязанское шоссе',
    'simferopolskoe-shosse': 'Симферопольское шоссе',
    'yaroslavskoe-shosse': 'Ярославское шоссе',
}

# Словарь для правильных названий городов на русском (с большой буквы)
RUSSIAN_CITIES = {
    'БАЛАШИХА': 'Балашиха',
    'ВИДНОЕ': 'Видное',
    'ДЗЕРЖИНСКИЙ': 'Дзержинский',
    'КОРОЛЕВ': 'Королев',
    'КОРОЛЁВ': 'Королев',
    'ДМИТРОВ': 'Дмитров',
    'ДОЛГОПРУДНЫЙ': 'Долгопрудный',
    'ЖЕЛЕЗНОДОРОЖНЫЙ': 'Железнодорожный',
    'ИВАНТЕЕВКА': 'Ивантеевка',
    'КЛИН': 'Клин',
    'КРАСНОАРМЕЙСК': 'Красноармейск',
    'КРАСНОГОРСК': 'Красногорск',
    'ЛОБНЯ': 'Лобня',
    'ЛЫТКАРИНО': 'Лыткарино',
    'МЫТИЩИ': 'Мытищи',
    'ОДИНЦОВО': 'Одинцово',
    'ПОДОЛЬСК': 'Подольск',
    'РЕУТОВ': 'Реутов',
    'СЕРГИЕВ ПОСАД': 'Сергиев Посад',
    'СОЛНЕЧНОГОРСК': 'Солнечногорск',
    'СОФРИНО': 'Софрино',
    'ФРЯЗИНО': 'Фрязино',
    'ХИМКИ': 'Химки',
    'ЩЕЛКОВО': 'Щелково',
    'ЩЕРБИНКА': 'Щербинка',
    'ЭЛЕКТРОСТАЛЬ': 'Электросталь',
    'НОГИНСК': 'Ногинск',
    'ПУШКИНО': 'Пушкино',
    'РАМЕНСКОЕ': 'Раменское',
    'ДОМОДЕДОВО': 'Домодедово',
    'МОСКВА': 'Москва',
    'МОСКОВСКАЯ ОБЛАСТЬ': 'Московская область',
    'НОВОРЯЗАНСКОЕ ШОССЕ': 'Новорязанское шоссе',
    'СИМФЕРОПОЛЬСКОЕ ШОССЕ': 'Симферопольское шоссе',
    'ЯРОСЛАВСКОЕ ШОССЕ': 'Ярославское шоссе',
}

def get_russian_city_name(city_name):
    """Получить название города на русском"""
    # Если город уже на русском
    city_upper = city_name.upper()
    if city_upper in RUSSIAN_CITIES:
        return RUSSIAN_CITIES[city_upper]
    
    # Если город на латинице, переводим
    city_lower = city_name.lower()
    if city_lower in LATIN_TO_RUSSIAN:
        return LATIN_TO_RUSSIAN[city_lower]
    
    # Если не нашли, возвращаем как есть
    return city_name

def fix_pages():
    """Основная функция исправления страниц"""
    
    print("="*80)
    print("ИСПРАВЛЕНИЕ СТРАНИЦ ЭВАКУАТОРОВ (РУССКИЕ НАЗВАНИЯ)")
    print("="*80)
    
    # Находим все страницы с типом 'service', 'truck_evacuator', 'manipulator'
    service_pages = Page.objects.filter(page_type__in=['service', 'truck_evacuator', 'manipulator'])
    total_pages = service_pages.count()
    
    print(f"\nНайдено страниц: {total_pages}")
    print("="*80)
    
    truck_count = 0
    manipulator_count = 0
    error_count = 0
    
    for page in service_pages:
        original_name = page.name
        name_upper = original_name.upper()
        
        print(f"\n[{truck_count + manipulator_count + 1}/{total_pages}] Обработка: {original_name}")
        
        # Определяем тип по названию
        if 'ГРУЗОВОЙ' in name_upper:
            # Извлекаем название города из текущего названия
            # Убираем "Грузовой эвакуатор" из названия
            city_part = original_name.replace('Грузовой эвакуатор', '').replace('грузовой эвакуатор', '')
            city_part = city_part.strip()
            
            # Если город на латинице или в неправильном регистре, переводим на русский
            russian_city = get_russian_city_name(city_part)
            
            # Формируем правильное название
            new_name = f"Грузовой эвакуатор {russian_city}"
            
            # Формируем slug
            city_slug = city_part.lower()
            # Проверяем в словаре латиницы
            for latin, russian in LATIN_TO_RUSSIAN.items():
                if city_part.lower() == latin or city_part.lower() in latin:
                    city_slug = latin
                    break
            else:
                city_slug = slugify(city_part.lower())
            
            new_slug = f"oblasti/gruzovoy-evakuator/gruzovoy-evakuator-{city_slug}"
            new_type = 'truck_evacuator'
            
            print(f"  ➜ Город: {city_part} -> {russian_city}")
            print(f"  ➜ Новое название: {new_name}")
            print(f"  ➜ Новый тип: {new_type}")
            print(f"  ➜ Новый slug: {new_slug}")
            
            # Проверяем уникальность slug
            if Page.objects.filter(slug=new_slug).exclude(id=page.id).exists():
                new_slug = f"{new_slug}-{page.id}"
                print(f"  ⚠ Slug уже существует, используем: {new_slug}")
            
            # Сохраняем
            try:
                page.name = new_name
                page.page_type = new_type
                page.slug = new_slug
                page.save()
                truck_count += 1
                print(f"  ✓ УСПЕШНО обновлен!")
            except Exception as e:
                error_count += 1
                print(f"  ✗ ОШИБКА: {e}")
                
        elif 'МАНИПУЛЯТОР' in name_upper or 'ЭВАКУАТОР-МАНИПУЛЯТОР' in name_upper:
            # Извлекаем название города из текущего названия
            city_part = original_name
            city_part = city_part.replace('Эвакуатор-манипулятор', '').replace('эвакуатор-манипулятор', '')
            city_part = city_part.replace('Манипулятор', '').replace('манипулятор', '')
            city_part = city_part.strip()
            
            # Если город на латинице или в неправильном регистре, переводим на русский
            russian_city = get_russian_city_name(city_part)
            
            # Формируем правильное название
            new_name = f"Эвакуатор-манипулятор {russian_city}"
            
            # Формируем slug
            city_slug = city_part.lower()
            # Проверяем в словаре латиницы
            for latin, russian in LATIN_TO_RUSSIAN.items():
                if city_part.lower() == latin or city_part.lower() in latin:
                    city_slug = latin
                    break
            else:
                city_slug = slugify(city_part.lower())
            
            new_slug = f"oblasti/manipulyator-{city_slug}"
            new_type = 'manipulator'
            
            print(f"  ➜ Город: {city_part} -> {russian_city}")
            print(f"  ➜ Новое название: {new_name}")
            print(f"  ➜ Новый тип: {new_type}")
            print(f"  ➜ Новый slug: {new_slug}")
            
            # Проверяем уникальность slug
            if Page.objects.filter(slug=new_slug).exclude(id=page.id).exists():
                new_slug = f"{new_slug}-{page.id}"
                print(f"  ⚠ Slug уже существует, используем: {new_slug}")
            
            # Сохраняем
            try:
                page.name = new_name
                page.page_type = new_type
                page.slug = new_slug
                page.save()
                manipulator_count += 1
                print(f"  ✓ УСПЕШНО обновлен!")
            except Exception as e:
                error_count += 1
                print(f"  ✗ ОШИБКА: {e}")
        else:
            print(f"  ⏭ ПРОПУЩЕН (не подходит под критерии)")
            continue
    
    # Выводим итоговую статистику
    print("\n" + "="*80)
    print("ИТОГОВАЯ СТАТИСТИКА:")
    print(f"  ✅ Грузовые эвакуаторы (truck_evacuator): {truck_count}")
    print(f"  ✅ Манипуляторы (manipulator): {manipulator_count}")
    print(f"  📊 Всего обновлено: {truck_count + manipulator_count}")
    print(f"  ❌ Ошибок: {error_count}")
    print("="*80)
    
    # Показываем примеры исправленных страниц
    print("\nПРИМЕРЫ ИСПРАВЛЕННЫХ СТРАНИЦ:")
    print("-"*80)
    
    truck_examples = Page.objects.filter(page_type='truck_evacuator')[:5]
    if truck_examples:
        print("\nГрузовые эвакуаторы:")
        for page in truck_examples:
            print(f"  • {page.name}")
            print(f"    Тип: {page.page_type}")
            print(f"    Slug: {page.slug}")
    
    manipulator_examples = Page.objects.filter(page_type='manipulator')[:5]
    if manipulator_examples:
        print("\nМанипуляторы:")
        for page in manipulator_examples:
            print(f"  • {page.name}")
            print(f"    Тип: {page.page_type}")
            print(f"    Slug: {page.slug}")
    
    print("\n✅ ГОТОВО!")
    print("="*80)

if __name__ == "__main__":
    print("\n🚀 Запуск скрипта исправления страниц...\n")
    fix_pages()