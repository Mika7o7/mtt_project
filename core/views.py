from django.shortcuts import render
from .models import MetaData, HeroSection, District, OrderStep, FormConfig, VideoReview, Photo, Price, Service, WhyChooseUs, FAQ, Rating, CalculatorOption


def index(request):
    """
    Renders the index page with data for all sections.
    """
    metadata = MetaData.objects.get(page='moscow_services')
    hero = HeroSection.objects.get(page='moscow_services')
    districts = District.objects.all()
    order_steps = OrderStep.objects.all()
    form_configs = FormConfig.objects.all()
    video_reviews = VideoReview.objects.all()
    photos = Photo.objects.all()
    prices = Price.objects.all()
    services = Service.objects.all()
    why_choose_us = WhyChooseUs.objects.all()
    faqs = FAQ.objects.all()[:6]
    rating = Rating.objects.get(page='moscow_services')
    calculator_options = CalculatorOption.objects.all()

    context = {
        'metadata': metadata,
        'hero': hero,
        'districts': districts,
        'order_steps': order_steps,
        'form_configs': form_configs,
        'video_reviews': video_reviews,
        'photos': photos,
        'prices': prices,
        'services': services,
        'why_choose_us': why_choose_us,
        'faqs': faqs,
        'rating': rating,
        'calculator_options': calculator_options,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def moscow_services(request):
    return render(request, 'about.html')

def airport(request):
    return render(request, 'about.html')

def passenger(request):
    return render(request, 'about.html')

def districts(request):
    return render(request, 'about.html')

def metro(request):
    return render(request, 'about.html')

def zelenograd(request):
    return render(request, 'about.html')

def novomoskovskiy(request):
    return render(request, 'about.html')

def troick(request):
    return render(request, 'about.html')

def privacy_policy(request):
    return render(request, 'about.html')

def online_payment(request):
    return render(request, 'about.html')

def cookies_policy(request):
    return render(request, 'about.html')

def uslugi(request):
    return render(request, 'about.html')