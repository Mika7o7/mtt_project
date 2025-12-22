# core/context_processors.py

from .models import MetroStation, District, City, TransportType, Gruzovoy, Manipulyator, Highway, Region

def menu_data(request):
    if request.path.startswith('/admin') or request.path.startswith('/static'):
        return {}

    return {
        'metro_stations': MetroStation.objects.only('name', 'slug').order_by('name'),
        'districts': District.objects.only('name', 'slug', 'short_name').order_by('name'),
        'oblast': Region.objects.only('name', 'slug').order_by('name'),
        'cities': City.objects.only('name', 'slug').order_by('name'),
        'transports': TransportType.objects.only('name', 'slug').order_by('name'),

        # НОВЫЕ — В МЕНЮ ДЛЯ ГРУЗОВЫХ, МАНИПУЛЯТОРОВ И ШОССЕ
        'gruzovoy_list': Gruzovoy.objects.only('name', 'slug').order_by('name'),
        'manipulyator_list': Manipulyator.objects.only('name', 'slug').order_by('name'),
        'highways': Highway.objects.only('name', 'slug').order_by('name'),
    }