# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MTT Project** — Django 5.2 веб-додаток для евакуаторної служби (російська мова).

**Тип проекту**: Django веб-додаток (не API-only)
**База даних**: SQLite3 (розробка), можлива міграція на іншу СКБ
**Управління залежностями**: Poetry
**Python версія**: >= 3.12

---

## 📋常见 Development Commands

### Встановлення залежностей
```bash
poetry install
poetry shell  # активувати віртуальне середовище
```

### Запуск локального сервера
```bash
python manage.py runserver
# або
poetry run python manage.py runserver
```

Сервер запускається на `http://127.0.0.1:8000`

### Міграції бази даних
```bash
# Створити міграції після змін у моделях
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Показати статус міграцій
python manage.py showmigrations
```

### Адміністрація
```bash
# Створити суперкористувача
python manage.py createsuperuser

# Доступ до адмін-панелі: http://127.0.0.1:8000/admin/
```

### Статичні файли
```bash
# Зібрати статичні файли для продакшену
python manage.py collectstatic
```
Статика знаходиться в `static/` (розробка) та збирається в `staticfiles/`.

### Form表单处理
```bash
# Усі форми обробляються через єдиний endpoint
POST /universal_form/
```

Цей endpoint обробляє такі типи форм:
- `fastorder` — швидкий заказ
- `callback` — запит на дзвінок
- `question` — питання
- `calculator` — заявка з калькулятора

---

## 🏗️ Code Architecture

### Загальна структура
```
mtt_project/
├── mtt_project/           # Проєкт Django
│   ├── settings.py        # Конфігурація (база, статика, CORS, middleware)
│   ├── urls.py            # Головні URL (тільки admin та core)
│   └── wsgi.py            # WSGI конфігурація
├── core/                  # Основний додаток
│   ├── admin.py           # Кастомна адмін-панель (організована в 3 розділи)
│   ├── models.py          # Всі моделі (Page, TransportType, Calculator тощо)
│   ├── views.py           # Вьюшки (універсальні, калькулятор, форми)
│   ├── urls.py            # URL маршрутизація (re_path для динамічних сторінок)
│   ├── context_processors.py  # Меню для шаблонів
│   ├── templatetags/      # Кастомні теги шаблонів
│   ├── templates/         # HTML шаблони
│   └── migrations/        # Міграції бази даних
├── pyproject.toml         # Poetry конфігурація (Django в dev-залежностях)
├── manage.py              # Django CLI
├── static/                # Статичні файли (CSS, JS, зображення)
├── media/                 # Завантажені файли
├── staticfiles/           # Зібрана статика (gitignore)
└── db.sqlite3             # База даних (розробка)
```

### Моделі (`core/models.py`)

**Ключові моделі:**

1. **Page** — універсальна модель сторінки з підтримкою різних типів:
   - `page_type` визначає тип (default, metro, district, region, highway, service, evacuator_city_mo, truck_evacuator, manipulator, special_equipment)
   - Має M2M зв'язки з усіма контент-моделями (hero_sections, transport_types, info_sections, faqs, articles тощо)
   - `slug` використовується для URL (головна сторінка має slug = "")
   - Реалізує `get_absolute_url()`

2. **TransportType** — типи транспорту з галереєю та цінами
3. **CalculatorVehicleType, CalculatorCategory, CalculatorExtraService** — мдель калькулятора
4. **HeroSection, HowToOrderStep, InfoSection, PriceItem, WorkPhoto, FAQ, Article** — блоки контенту

**Важливо:**
- Моделі використовують blank=True, null=True для slug у TransportType
- ManyToMany fields мають `related_name` для зворотного доступу
- Є валідація через `clean()` для Page (тільки одна головна сторінка)

### Views (`core/views.py`)

**Universal view pattern:**
- `home()` — головна сторінка (Page з is_homepage=True)
- `page_detail(path)` — динамічні сторінки по slug (re_path `^(?P<path>.*)/$`)
- `transport_detail(slug)` — детальна сторінка типу транспорту
- `universal_form()` — POST endpoint для всіх форм
- `policy()` — політика конфіденційності

**Калькулятор:**
- Дані завантажуються з моделей `CalculatorVehicleType`, `CalculatorCategory`, `CalculatorExtraService`
- Групування по `vehicle_type` (evacuator/manipulator)
- Сортування по полях `order`

**Телеграм інтеграція:**
- Форми відправляються в Telegram через `universal_form`
- Токен та chat_id захардкожені (потрібно винести в settings)

### URL Routing (`core/urls.py`)

Порядок маршрутизації важливий:
```python
urlpatterns = [
    path('articles/<int:pk>/', views.article_detail),
    path('universal_form/', views.universal_form),
    path('politika-cookies/', TemplateView...),
    path('policy/', views.policy),
    path('transport/<slug:slug>/', views.transport_detail),
    re_path(r'^(?P<path>.*)/$', views.page_detail),  # caught all
    path('', views.page_detail),  # homepage
]
```

### Адмін-панель (`core/admin.py`)

Кастомний `CustomAdminSite` організований у 3 розділи:
1. **Модулі** — HeroSection, HowToOrderStep, TransportType, WhyChooseUs, InfoSection, PriceItem, WorkPhoto, FAQ, Article
2. **Калькулятор** — CalculatorVehicleType, CalculatorCategory, CalculatorExtraService
3. **Страницы** — Page

**Особливості:**
- `TransportTypeAdmin` — slug автозаповнення (`prepopulated_fields`)
- `PageAdmin` — кастомна форма `PageAdminForm` з валідацією slug
- `PageAdmin.get_search_results()` — нормалізація регістру пошуку для SQLite
- `filter_horizontal` для M2M полів

### Context Processor (`core/context_processors.py`)

Додає в контекст всіх шаблонів меню:
- `metro_pages`, `district_pages`, `region_pages`, `city_pages`, `gruz_pages`, `manip_pages`, `highway_pages` — відфільтровані Page за типом
- `transports` — всі TransportType

Використовується в `base.html` для навігації.

### Template Tags (`core/templatetags/dict_extras.py`)

Простий тег `get_item` для доступу до словника в шаблоні:
```django
{% load dict_extras %}
{{ my_dict|get_item:key }}
```

---

## 🎨 Frontend Architecture

**Шаблонізатор:** Django Templates (not a SPA)

**Основні шаблони:**
- `base.html` — базовий шаблон з `{% block content %}`, підключає CSS/JS
- `page_detail.html` — головний шаблон для відображення Page з усіма пов'язаними об'єктами
- `transport_detail.html` — детальна сторінка транспорту
- `article_detail.html` — стаття
- `header.html` — навігаційне меню (інклюд)
- `footer.html` — футер

**CSS/JS:** знаходиться в `static/assets/`

**Калькулятор:** реалізований у `page_detail.html` через JavaScript, дані передаються через context.

---

## 🔗 External Integrations

- **Telegram Bot API** — надсилання повідомлень з форм (`core/views.py`)
  - Токен та chat_id захардкожені (IDER: перенести в settings або .env)
- **CORS** — `django-cors-headers`, дозволені origin в settings.py

---

## ⚙️ Configuration (`mtt_project/settings.py`)

**Важливі налаштування:**
- `DEBUG = True` (розробка)
- `ALLOWED_HOSTS` — включно з IP сервера та доменом (для продакшену)
- `DATABASES` — SQLite3
- `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`
- `MEDIA_URL`, `MEDIA_ROOT`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS` — домени для продакшену + localhost:8000
- `INSTALLED_APPS` — додаток `core`, `corsheaders`
- `MIDDLEWARE` — включає `checkpost.middleware.CheckpostMiddleware` (не існує в репозиторії!)

**⚠️ Увага:** `checkpost.middleware.CheckpostMiddleware` посилається на неіснуючий модуль. Перевірте, чи потрібен він.

---

## 🧪 Testing

**Тестів у репозиторії немає.** Для запуску тестів Django:
```bash
python manage.py test
```

Для запуску окремого тесту:
```bash
python manage.py test core.tests.TestClassName
```

---

## 📦 Dependencies

**pyproject.toml:**
- `django` (>=5.2.6, <6.0.0) — у dev-групі
- `pillow` — обробка зображень
- `requests` — HTTP запити (Telegram)
- `django-cors-headers` — CORS підтримка

Установка: `poetry install`

---

## 🗄️ Database Schema Quick Reference

- **Page** — основна модель сторінок, зв'язок M2M з усім контентом
- **TransportType** — типи евакуаторів/маніпуляторів
- **CalculatorVehicleType** — групування для калькулятора
- **CalculatorCategory** — категорії послуг (ціна за 100км)
- **CalculatorExtraService** — додаткові опції
- **HeroSection, HowToOrderStep, WhyChooseUs, InfoSection, PriceItem, WorkPhoto, FAQ, Article** — контентні блоки

---

## 🚀 Deployment Notes

1. Збір статики: `python manage.py collectstatic`
2. Налаштуйте `DEBUG=False` в settings.py або через env-змінну
3. Переконайтесь, `ALLOWED_HOSTS` містить домен
4. Переконайтесь, `CSRF_TRUSTED_ORIGINS` налаштовано для HTTPS домену
5. База даних SQLite може не підходити для продакшену — ро look миграція на PostgreSQL

---

## 🐛 Known Issues

1. **checkpost middleware** посилається на неіснуючий модуль — можливо, старі залишки
2. Токен Telegram захардкожений у `core/views.py` — винести в settings або .env
3. Slug у `TransportType` має `blank=True, null=True`, але `unique=True` — це може викликати проблеми при створенні (нумерація)
4. Немає тестів
5. README.md порожній

---

## 📝 Style Conventions

- **Python:** стандартний PEP 8, імпорти в alphabet order
- **Django:** використання function-based views (не class-based)
- **Моделі:** capitalized, singular, Cyrillic `verbose_name`
- **Шаблони:** Django Template Language, base.html → block content
- **Міграції:** створювати після змін моделей (`python manage.py makemigrations`)
