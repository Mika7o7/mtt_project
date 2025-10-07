from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contacts/', views.contacts, name='contacts'),
    path('moscow_services/', views.moscow_services, name='moscow_services'),
    path('airport/', views.airport, name='airport'),
    path('passenger/', views.passenger, name='passenger'),
    path('districts/', views.districts, name='districts'),
    path('metro/', views.metro, name='metro'),
    path('zelenograd/', views.zelenograd, name='zelenograd'),
    path('novomoskovskiy/', views.novomoskovskiy, name='novomoskovskiy'),
    path('troick/', views.troick, name='troick'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('online_payment/', views.online_payment, name='online_payment'),
    path('cookies_policy/', views.cookies_policy, name='cookies_policy'),
    path('uslugi/', views.uslugi, name='uslugi'),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('submit_calculator/', views.submit_calculator, name='submit_calculator'),

    


    # path('online-payment/', views.online_payment, name='online_payment'),
    # path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    # path('cookies-policy/', views.cookies_policy, name='cookies_policy'),
    # Add other URL patterns
]