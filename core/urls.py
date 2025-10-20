from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('company/', views.company, name='company'),
    path('prices/', views.prices, name='prices'),
    path('gallery/', views.gallery, name='gallery'),
    path('calculator/', views.calculator, name='calculator'),

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