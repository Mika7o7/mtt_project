from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Главная (если есть отдельная view для главной)
    # path('', views.home, name='home'),
    
    # Все СТАТИЧНЫЕ пути
    path('services/', views.services, name='services'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('metro/', views.metro_list, name='metro_list'),
    
    path('submit_form/', views.submit_form, name='submit_form'),
    path('send_callback/', views.send_callback, name='send_callback'),
    path('send_callback_question/', views.send_callback_question, name='send_callback_question'),
    path('politika-cookies/', TemplateView.as_view(template_name='politika-cookies.html'), name='politika-cookies'),
    path('policy/', views.policy, name='policy'),
    
    # ДИНАМИЧЕСКИЕ пути со slug (специфичные)
    path('transport/<slug:slug>/', views.transport_detail, name='transport_detail'),
    
    # Области/округа/города и т.д. - ВСЕ ЭТИ ПУТИ ДОЛЖНЫ БЫТЬ ВЫШЕ общего <slug:slug>
    path('oblasti/<slug:slug>/', views.location_detail, name='districts'),
    path('oblasti/moskovskaya-oblast/<slug:slug>/', views.location_detail, name='oblasti'),
    path('oblasti/evakuator-metro/<slug:slug>/', views.location_detail, name='metro_detail'),
    path('oblasti/evakuator/<slug:slug>/', views.location_detail, name='city_detail'),
    path('oblasti/gruzovoy-evakuator/<slug:slug>/', views.location_detail, name='gruzovoy_detail'),
    # УДАЛИТЕ этот дублирующий путь или измените его:
    # path('oblasti/<slug:slug>/', views.location_detail, name='manipulyator_detail'),  # ← ДУБЛИКАТ!
    path('oblasti/manipulyator/<slug:slug>/', views.location_detail, name='manipulyator_detail'),  # ← ИСПРАВЬТЕ
    path('oblasti/evakuatoryi-shosse/<slug:slug>/', views.location_detail, name='highway_detail'),
    
    # ОБЩИЙ путь для страниц Page - САМЫЙ ПОСЛЕДНИЙ!
    path('<slug:slug>/', views.page_detail, name='page_detail'),  # ← ДОБАВЬТЕ / в конце!
    path('', views.page_detail, name='page_detail'),  # ← ДОБАВЬТЕ / в конце!
    
]