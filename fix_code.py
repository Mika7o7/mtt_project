#!/usr/bin/env python
import os
import django
import re
from django.db.models import Count, Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtt_project.settings')
django.setup()

from core.models import Page

def find_duplicates():
    """Находит дубликаты страниц по названию (регистронезависимо)"""
    
    print("=" * 60)
    print("ПОИСК ДУБЛИКАТОВ СТРАНИЦ")
    print("=" * 60)
    
    # Исключаем обычные страницы (default)
    pages = Page.objects.exclude(page_type='default')
    
    # Группируем по названию (в нижнем регистре)
    from django.db.models.functions import Lower
    
    duplicates = []
    seen = {}
    
    for page in pages:
        if not page.name:
            continue
            
        name_lower = page.name.lower().strip()
        
        if name_lower in seen:
            seen[name_lower].append(page)
        else:
            seen[name_lower] = [page]
    
    # Собираем только те, у которых больше одного
    for name_lower, page_list in seen.items():
        if len(page_list) > 1:
            duplicates.append({
                'name': page_list[0].name,
                'name_lower': name_lower,
                'pages': page_list,
                'count': len(page_list)
            })
    
    if duplicates:
        print(f"\n❌ Найдено дубликатов: {len(duplicates)}")
        for dup in duplicates:
            print(f"\n📌 Название: {dup['name']}")
            print(f"   Количество: {dup['count']}")
            print("   Страницы:")
            for page in dup['pages']:
                print(f"     - ID: {page.id}, Тип: {page.page_type}, Slug: {page.slug}")
    else:
        print("\n✅ Дубликатов не найдено!")
    
    return duplicates

def fix_duplicates():
    """Удаляет дубликаты страниц, оставляя по одной"""
    
    print("=" * 60)
    print("УДАЛЕНИЕ ДУБЛИКАТОВ СТРАНИЦ")
    print("=" * 60)
    
    # Исключаем обычные страницы
    pages = Page.objects.exclude(page_type='default')
    
    # Группируем по названию (в нижнем регистре)
    seen = {}
    deleted_count = 0
    kept_count = 0
    
    for page in pages:
        if not page.name:
            continue
            
        name_lower = page.name.lower().strip()
        
        if name_lower in seen:
            seen[name_lower].append(page)
        else:
            seen[name_lower] = [page]
    
    # Обрабатываем каждую группу дубликатов
    for name_lower, page_list in seen.items():
        if len(page_list) > 1:
            print(f"\n📌 Название: {page_list[0].name}")
            print(f"   Найдено дубликатов: {len(page_list)}")
            
            # Сортируем по ID (оставляем самую старую)
            page_list.sort(key=lambda x: x.id)
            
            # Оставляем первую (самую старую)
            keep_page = page_list[0]
            delete_pages = page_list[1:]
            
            print(f"   ✅ Оставляем ID: {keep_page.id} (самый старый)")
            
            for page in delete_pages:
                print(f"   ❌ Удаляем ID: {page.id}")
                page.delete()
                deleted_count += 1
            
            kept_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"Оставлено уникальных страниц: {kept_count}")
    print(f"Удалено дубликатов: {deleted_count}")
    print(f"{'=' * 60}")
    
    return deleted_count

def fix_info_names():
    """Исправляет поле info_name у всех страниц"""
    
    print("=" * 60)
    print("ИСПРАВЛЕНИЕ ПОЛЯ INFO_NAME")
    print("=" * 60)
    
    pages = Page.objects.all()
    updated_count = 0
    
    for page in pages:
        if not page.info_name:
            continue
            
        old_info_name = page.info_name
        new_info_name = old_info_name
        
        print(f"\nID: {page.id}")
        print(f"Тип: {page.page_type}")
        print(f"Slug: {page.slug}")
        print(f"Старое info_name: {old_info_name}")
        
        # Проверяем, есть ли у нас правило для этого типа страниц
        fixed = False
        
        # 1. Для метро
        if page.page_type == 'metro' or (page.slug and 'metro' in page.slug):
            # Убираем "Эвакуатор " в начале
            if old_info_name.startswith('Эвакуатор '):
                new_info_name = old_info_name[10:]  # len('Эвакуатор ') = 10
                fixed = True
                print(f"  Метро: убираем 'Эвакуатор'")
            
            # Убираем " (метро)" в конце
            if new_info_name.endswith(' (метро)'):
                new_info_name = new_info_name[:-8]  # len(' (метро)') = 8
                fixed = True
                print(f"  Метро: убираем ' (метро)'")
        
        # 2. Для городов (обычные страницы с evakuator в slug)
        elif page.page_type == 'default' and page.slug and 'evakuator' in page.slug:
            if old_info_name.startswith('Эвакуатор '):
                new_info_name = old_info_name[10:]
                fixed = True
                print(f"  Города: убираем 'Эвакуатор'")
        
        # 3. Для областей
        elif page.page_type == 'region':
            if old_info_name.startswith('Эвакуатор '):
                new_info_name = old_info_name[10:]
                fixed = True
                print(f"  Области: убираем 'Эвакуатор'")
        
        # 4. Для грузовых
        elif page.page_type == 'service' and page.slug and 'gruzovoy' in page.slug:
            if old_info_name.startswith('Грузовой эвакуатор '):
                new_info_name = old_info_name[19:]  # len('Грузовой эвакуатор ') = 19
                fixed = True
                print(f"  Грузовые: убираем 'Грузовой эвакуатор'")
        
        # 5. Для манипуляторов
        elif page.page_type == 'service' and page.slug and 'manipulyator' in page.slug:
            if old_info_name.startswith('Эвакуатор с манипулятором '):
                new_info_name = old_info_name[26:]  # len('Эвакуатор с манипулятором ') = 26
                fixed = True
                print(f"  Манипуляторы: убираем 'Эвакуатор с манипулятором'")
        
        # 6. Для шоссе
        elif page.page_type == 'highway':
            if old_info_name.startswith('Эвакуатор на '):
                new_info_name = old_info_name[13:]  # len('Эвакуатор на ') = 13
                # Добавляем "ЭВАКУАТОР НА" в начало
                new_info_name = 'ЭВАКУАТОР НА ' + new_info_name
                fixed = True
                print(f"  Шоссе: заменяем на 'ЭВАКУАТОР НА'")
        
        # 7. Если есть дублирование "Эвакуатор ЭВАКУАТОР" в любом месте
        if not fixed and 'Эвакуатор ЭВАКУАТОР' in old_info_name:
            new_info_name = old_info_name.replace('Эвакуатор ЭВАКУАТОР', 'ЭВАКУАТОР', 1)
            fixed = True
            print(f"  Универсальное: убираем дублирование")
        
        # 8. Если начинается с "Эвакуатор " (универсальное правило)
        if not fixed and old_info_name.startswith('Эвакуатор '):
            new_info_name = old_info_name[10:]
            fixed = True
            print(f"  Универсальное: убираем 'Эвакуатор' в начале")
        
        # Дополнительная чистка
        if fixed:
            # Убираем множественные пробелы
            new_info_name = re.sub(r'\s+', ' ', new_info_name)
            # Убираем пробелы в начале и конце
            new_info_name = new_info_name.strip()
            
            # Проверяем, что название не пустое
            if new_info_name:
                page.info_name = new_info_name
                page.save()
                updated_count += 1
                print(f"✅ Новое info_name: {new_info_name}")
            else:
                print(f"⚠️  Предупреждение: новое название пустое, оставляем старое")
        else:
            print(f"  Без изменений")
    
    print(f"\n{'=' * 60}")
    print(f"Всего обновлено страниц: {updated_count}")
    print(f"{'=' * 60}")

def check_problems():
    """Проверяет проблемы в данных"""
    
    print("=" * 60)
    print("ПРОВЕРКА ПРОБЛЕМ В ДАННЫХ")
    print("=" * 60)
    
    # Проверка дубликатов по названиям
    duplicates = find_duplicates()
    
    # Проверка проблем в info_name
    pages = Page.objects.all()
    problems = []
    
    problematic_patterns = [
        'Эвакуатор ЭВАКУАТОР',
        'Грузовой эвакуатор ГРУЗОВОЙ ЭВАКУАТОР',
        'Эвакуатор с манипулятором МАНИПУЛЯТОР',
        'Эвакуатор на ЭВАКУАТОР',
    ]
    
    for page in pages:
        if not page.info_name:
            continue
            
        info_name = page.info_name
        
        for pattern in problematic_patterns:
            if pattern in info_name:
                problems.append({
                    'id': page.id,
                    'type': page.page_type,
                    'slug': page.slug,
                    'name': info_name,
                    'pattern': pattern
                })
                break
    
    if problems:
        print(f"\n❌ Найдено проблем с info_name: {len(problems)}")
        for prob in problems[:10]:
            print(f"\nID: {prob['id']}")
            print(f"Тип: {prob['type']}")
            print(f"Slug: {prob['slug']}")
            print(f"info_name: {prob['name']}")
            print(f"Проблема: {prob['pattern']}")
        if len(problems) > 10:
            print(f"... и еще {len(problems) - 10} проблем")
    else:
        print("\n✅ Проблем с info_name не найдено")
    
    return duplicates, problems

if __name__ == "__main__":
    print("1. Проверить проблемы")
    print("2. Удалить дубликаты страниц (кроме обычных)")
    print("3. Исправить info_name")
    print("4. Сделать всё сразу")
    
    choice = input("Выберите действие (1-4): ")
    
    if choice == '1':
        check_problems()
    elif choice == '2':
        duplicates = find_duplicates()
        if duplicates:
            print(f"\nНайдено {len(duplicates)} групп дубликатов")
            confirm = input("Удалить все дубликаты? (y/n): ")
            if confirm.lower() == 'y':
                fix_duplicates()
            else:
                print("Операция отменена")
        else:
            print("Дубликатов не найдено")
    elif choice == '3':
        confirm = input("Исправить info_name для всех страниц? (y/n): ")
        if confirm.lower() == 'y':
            fix_info_names()
    elif choice == '4':
        print("\n=== ШАГ 1: Проверка проблем ===")
        duplicates, problems = check_problems()
        
        if duplicates:
            print("\n=== ШАГ 2: Удаление дубликатов ===")
            fix_duplicates()
        
        if problems:
            print("\n=== ШАГ 3: Исправление info_name ===")
            fix_info_names()
        
        print("\n=== ШАГ 4: Финальная проверка ===")
        check_problems()
    else:
        print("Неверный выбор")