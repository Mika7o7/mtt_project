from django.shortcuts import render, get_object_or_404
from .models import Page, Service, Document, Review

def index(request):
    services = Service.objects.all()[:5]  # Показать 5 услуг на главной
    photos = ["photo 1","photo 2","photo 3","photo 4"]
    prices = [1,2,3,4]
    context = {'services': services, "photos": photos, "prices": prices}
    return render(request, 'index.html', {'services': services})

def about(request):
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

def cookies_policy  (request):
    return render(request, 'about.html')

def page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'generic_page.html', {'page': page})

def services(request):
    services = Service.objects.all()
    return render(request, 'uslugi-evakuatora.html', {'services': services})

def documents(request):
    documents = Document.objects.all()
    return render(request, 'documents.html', {'documents': documents})

def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'otzyvy.html', {'reviews': reviews})