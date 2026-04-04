from .models import Page, TransportType
from django.db.models import Q
from django.conf import settings

def menu_data(request):
    if request.path.startswith('/admin') or request.path.startswith('/static'):
        return {}

    return {
        'metro_pages': Page.objects.filter(
            page_type='metro',
            is_active=True
        ).only('name', 'slug').order_by('name'),

        'district_pages': Page.objects.filter(
            page_type='district',
            is_active=True
        ).only('name', 'slug').order_by('name'),

        'region_pages': Page.objects.filter(
            page_type='region',
            is_active=True
        ).only('name', 'slug').order_by('name'),

        'city_pages': Page.objects.filter(
            page_type='evacuator_city_mo',
            is_active=True
        ).only('name', 'slug').order_by('name'),

        # Грузовые эвакуаторы - новый тип + старые для совместимости
        'gruz_pages': Page.objects.filter(
            Q(page_type='truck_evacuator') |
            Q(page_type='service', name__icontains='Грузовой'),
            is_active=True
        ).only('name', 'slug').order_by('name'),

        # Манипуляторы - новый тип + старые для совместимости
        'manip_pages': Page.objects.filter(
            Q(page_type='manipulator') |
            Q(page_type='service', name__icontains='манипулятор'),
            is_active=True
        ).only('name', 'slug').order_by('name'),

        'highway_pages': Page.objects.filter(
            page_type='highway',
            is_active=True
        ).only('name', 'slug').order_by('name'),

        'transports': TransportType.objects.only('name', 'slug').order_by('name'),
    }


def recaptcha_data(request):
    """Додає ключ reCAPTCHA v3 в контекст усіх шаблонів"""
    return {
        'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_SITE_KEY', ''),
    }