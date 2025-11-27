from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('articles/', views.article_list, name='articles'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('prices/', views.prices, name='prices'),
    path('gallery/', views.gallery, name='gallery'),
    path('calculator/', views.calculator, name='calculator'),
    path('transport/<slug:slug>/', views.transport_detail, name='transport_detail'),
    path('okrug/', views.district_list, name='district_list'),
    path('metro/', views.metro_list, name='metro_list'),
    path('payment/', views.payment, name='payment'),

    path('district/<slug:slug>/', views.location_detail, name='district_detail'),
    path('metro/<slug:slug>/', views.location_detail, name='metro_detail'),
    path('city/<slug:slug>/', views.location_detail, name='city_detail'),

    # path('cookies_policy/', views.cookies_policy, name='cookies_policy'),
    # path('uslugi/', views.uslugi, name='uslugi'),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('send_callback/', views.send_callback, name='send_callback'),
    path('send_callback_question/', views.send_callback_question, name='send_callback_question'),

    
    


    # path('online-payment/', views.online_payment, name='online_payment'),
    # path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    # path('cookies-policy/', views.cookies_policy, name='cookies_policy'),
    # Add other URL patterns
]