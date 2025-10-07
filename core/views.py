from django.shortcuts import render
from .models import MetaData, HeroSection, District, OrderStep, FormConfig, VideoReview, Photo, Price, Service, WhyChooseUs, FAQ, Rating, CalculatorOption


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # если хочешь, но лучше убрать и использовать token в форме

TELEGRAM_TOKEN = "1625085576:AAGR1VzsLToXxe5NxiPGA-IZy1NmQlbNX7U"  # или хранить в settings.SECRET
TELEGRAM_CHAT_ID = "1628997906"

@csrf_exempt  # если оставляешь csrf в форме, можно убрать csrf_exempt
def submit_form(request):
    if request.method == "POST":
        name = request.POST.get("f_name", "").strip()
        phone = request.POST.get("f_phone", "").strip()
        auto = request.POST.get("f_auto", "").strip()
        # можно добавить валидацию: если нет телефона — вернуть ошибку
        if not phone:
            return JsonResponse({"success": False, "message": "Укажите, пожалуйста, телефон."})

        message = (
            "🚨 <b>Новая заявка с сайта</b>\n\n"
            f"👤 Имя: {name or '—'}\n"
            f"📞 Телефон: {phone}\n"
            f"🚗 Авто: {auto or '—'}"
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        }
        try:
            r = requests.post(url, data=payload, timeout=5)
            r.raise_for_status()
            return JsonResponse({"success": True, "message": "Спасибо! Заявка отправлена."})
        except Exception as e:
            # логируй e
            return JsonResponse({"success": False, "message": "Не удалось отправить сообщение в Telegram."})

    return JsonResponse({"success": False, "message": "Некорректный запрос"}, status=400)


@csrf_exempt  # если ты используешь CSRF в форме — убери этот декоратор
def submit_calculator(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Только POST"}, status=400)

    # получим поля — изменяй имена если нужно
    name = request.POST.get("f_name", "").strip()
    phone = request.POST.get("f_phone", "").strip()
    vk = request.POST.get("calc_vk", "")
    km = request.POST.get("calc_km", "")
    total = request.POST.get("calc_total", "")
    extras = request.POST.get("calc_extras", "")
    comment = request.POST.get("f_comment", "")

    # валидация
    if not phone:
        return JsonResponse({"success": False, "message": "Укажите телефон"})

    # Формируем сообщение в Telegram
    message = (
        "🚗 <b>Заявка из калькулятора</b>\n"
        f"👤 Имя: {name or '—'}\n"
        f"📞 Телефон: {phone}\n"
        f"Тип: {vk}\n"
        f"Км: {km}\n"
        f"Доп. опции сумма: {extras}\n"
        f"Итог: {total} руб.\n"
        f"Комментарий: {comment or '—'}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}

    try:
        r = requests.post(url, data=payload, timeout=5)
        r.raise_for_status()
    except Exception as e:
        # логирование (print или logger) если нужно
        print("Telegram send error:", e)
        return JsonResponse({"success": False, "message": "Не удалось отправить сообщение. Попробуйте позже."})

    return JsonResponse({"success": True, "message": "Спасибо! Заявка отправлена."})


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

def test(request):
    return render(request, 'test.html')

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