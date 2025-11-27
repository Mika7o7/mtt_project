# core/context_processors.py
from .models import MetroStation, District, City, TransportType

def menu_data(request):
    if request.path.startswith('/admin') or request.path.startswith('/static'):
        return {}

    return {
        'metro_stations': MetroStation.objects.only('name', 'slug').order_by('name'),
        'districts': District.objects.only('name', 'slug', 'short_name').order_by('name'),
        'cities': City.objects.only('name', 'slug').order_by('name'),  # ← НОВОЕ!
        'transports': TransportType.objects.only('name', 'slug').order_by('name'),
    }