from django.shortcuts import render, get_object_or_404
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto, FAQ, Rating, Article
)

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # если хочешь, но лучше убрать и использовать token в форме

TELEGRAM_TOKEN = "1625085576:AAGR1VzsLToXxe5NxiPGA-IZy1NmQlbNX7U"  # или хранить в settings.SECRET
TELEGRAM_CHAT_ID = "1628997906"
@csrf_exempt
def submit_form(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Некорректный запрос"}, status=400)

    # Основные поля
    name = request.POST.get("f_name", "").strip()
    phone = request.POST.get("f_phone", "").strip()
    name2 = request.POST.get("f_name_2", "").strip()
    phone2 = request.POST.get("f_phone_2", "").strip()
    comment = request.POST.get("f_ztxt", "").strip()
    distance = request.POST.get("f_qq", "").strip()
    vk_type = request.POST.get("clt_vk", "").strip()
    auto_type_id = request.POST.get("clt_vid_1", "").strip()
    koleso = request.POST.get("f_koleso", "").strip()
    mesto = request.POST.get("f_mesto", "").strip()
    mesto_cd = request.POST.get("f_mesto_cd", "").strip()
    end = request.POST.get("f_end", "").strip()
    end_cd = request.POST.get("f_end_cd", "").strip()
    date = request.POST.get("f_date", "").strip()
    time = request.POST.get("f_time", "").strip()

    # Проверяем телефон
    if not phone:
        return JsonResponse({"success": False, "message": "Укажите номер телефона."})

    # --- Словарь видов авто ---
    AUTO_TYPES = {
        "1": "Седан",
        "2": "Мотоцикл",
        "3": "Кроссовер",
        "4": "Минивэн",
        "5": "Внедорожник",
        "6": "Премиум класс",
        "7": "Спорт класс",
        "8": "Микроавтобус",
        "9": "Коммерческий транспорт",
        "10": "Легкая спецтехника до 5 тонн",
    }

    auto_type_name = AUTO_TYPES.get(auto_type_id, "—")

    # --- Словарь доп. опций ---
    dop_map = {
        "f_dop_1_1": "Нет буксировочного крюка",
        "f_dop_1_2": "Необходимо прикурить авто",
        "f_dop_1_3": "Заблокирован руль",
        "f_dop_1_4": "ТС в подземном паркинге",
        "f_dop_1_5": "Клиренс менее 15 см",
        "f_dop_1_6": "Автомобиль в ряду",
        "f_dop_2_1": "Машина стоит вплотную к бордюру",
        "f_dop_2_2": "Необходимо снять с автовоза",
        "f_dop_2_3": "Автомобиль в ряду",
    }

    # --- Собираем отмеченные опции ---
    extras = [label for key, label in dop_map.items() if request.POST.get(key) == "1"]
    extras_text = ", ".join(extras) if extras else "—"

    # --- Формируем сообщение ---
    message = (
        f"🚨 <b>Новая заявка с сайта</b>\n\n"
        f"👤 Имя: {name or '—'}\n"
        f"📞 Телефон: {phone or '—'}\n"
        f"👥 Доп. контакт: {name2 or '—'} / {phone2 or '—'}\n"
        f"🚗 Тип техники: {'Эвакуатор' if vk_type == '1' else 'Манипулятор'}\n"
        f"🚘 Вид авто: {auto_type_name}\n"
        f"🔩 Кол-во колёс: {koleso or '—'}\n"
        f"📍 Откуда: {mesto or mesto_cd or '—'}\n"
        f"🏁 Куда: {end or end_cd or '—'}\n"
        f"📏 Расстояние: {distance or '—'} км\n"
        f"🧰 Доп. опции: {extras_text}\n"
        f"🕒 Дата/время: {date or '—'} {time or ''}\n"
        f"💬 Комментарий: {comment or '—'}"
    )

    # --- Отправляем в Telegram ---
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
            timeout=5,
        )
        r.raise_for_status()
        return JsonResponse({"success": True, "message": "Спасибо! Ваша заявка успешно отправлена."})
    except Exception as e:
        print("Ошибка Telegram:", e)
        return JsonResponse({"success": False, "message": "Не удалось отправить сообщение в Telegram."})



@csrf_exempt  # если ты используешь CSRF в форме — убери этот декоратор
def send_callback(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Только POST"}, status=400)

    # получим поля — изменяй имена если нужно
    name = request.POST.get("name", "").strip()
    phone = request.POST.get("phone", "").strip()
   

    # валидация
    if not phone:
        return JsonResponse({"success": False, "message": "Укажите телефон"})

    # Формируем сообщение в Telegram
    message = (
        "🚗 <b>Заявка на звонок</b>\n"
        f"👤 Имя: {name or '—'}\n"
        f"📞 Телефон: {phone}\n"
      
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


@csrf_exempt
def send_callback_question(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Только POST"}, status=400)

    name = request.POST.get("q_name", "").strip()
    phone = request.POST.get("q_phone", "").strip()
    question = request.POST.get("q_question", "").strip()

    if not phone:
        return JsonResponse({"success": False, "message": "Укажите телефон"})

    message = (
        "📩 <b>Заявка с сайта</b>\n"
        f"👤 Имя: {name or '—'}\n"
        f"📞 Телефон: {phone}\n"
    )

    if question:
        message += f"❓ Вопрос: {question}\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}

    try:
        r = requests.post(url, data=payload, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print("Telegram send error:", e)
        return JsonResponse({"success": False, "message": "Не удалось отправить сообщение. Попробуйте позже."})

    return JsonResponse({"success": True, "message": "Спасибо! Ваш вопрос отправлен."})



def index(request):
    """
    Renders the index page with data for all sections.
    """
    hero = HeroSection.objects.first()
    order_steps = HowToOrderStep.objects.all()
    transports = TransportType.objects.all()
    info = InfoSection.objects.first()
    prices = PriceItem.objects.all()
    why_choose_us = WhyChooseUs.objects.all()
    photos = WorkPhoto.objects.all()
    faqs = FAQ.objects.filter(is_active=True)[:6]
    rating = Rating.objects.first()  # если есть модель Rating


    # Создаём список звезд для шаблона
    rating_stars = list(range(1, 6))  # [1, 2, 3, 4, 5]


    context = {
        'hero': hero,
        'order_steps': order_steps,
        'transports': transports,
        'info': info,
        'prices': prices,
        'why_choose_us': why_choose_us,
        'photos': photos,
        'faqs': faqs,
        'rating': rating,
        'rating_stars': rating_stars,
    }
    return render(request, 'test.html', context)

def test(request):
    return render(request, 'test.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    info = InfoSection.objects.first()
    photos = WorkPhoto.objects.all()

    context = {
        'info': info,
        'photos': photos,
    }

    return render(request, 'about.html', context)

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})

def prices(request):
    return render(request, 'prices.html')

def gallery(request):
    return render(request, 'gallery.html')

def calculator(request):
    return render(request, 'calculator.html')