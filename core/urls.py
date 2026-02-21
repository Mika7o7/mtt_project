from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    
    # Все СТАТИЧНЫЕ пути
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    
    path('universal_form/', views.universal_form, name='universal_form'),
    path('politika-cookies/', TemplateView.as_view(template_name='politika-cookies.html'), name='politika-cookies'),
    path('policy/', views.policy, name='policy'),
    
    # ДИНАМИЧЕСКИЕ пути со slug (специфичные)
    path('transport/<slug:slug>/', views.transport_detail, name='transport_detail'),
    
    
    # ОБЩИЙ путь для страниц Page - САМЫЙ ПОСЛЕДНИЙ!
    path('<slug:slug>/', views.page_detail, name='page_detail'),  # ← ДОБАВЬТЕ / в конце!
    path('', views.page_detail, name='page_detail'),  # ← ДОБАВЬТЕ / в конце!
    
]