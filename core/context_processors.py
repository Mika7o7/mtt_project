# core/context_processors.py

from .models import Page, TransportType

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
            page_type='city',
            is_active=True
        ).only('name', 'slug').order_by('name'),
        
        'gruz_pages': Page.objects.filter(
            page_type='service',
            name__icontains='Грузовой',
            is_active=True
        ).only('name', 'slug').order_by('name'),
        
        'manip_pages': Page.objects.filter(
            page_type='service',
            name__icontains='манипулятор',
            is_active=True
        ).only('name', 'slug').order_by('name'),
        
        'highway_pages': Page.objects.filter(
            page_type='highway',
            is_active=True
        ).only('name', 'slug').order_by('name'),
        
        'transports': TransportType.objects.only('name', 'slug').order_by('name'),
    }