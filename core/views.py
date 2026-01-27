from django.shortcuts import render, get_object_or_404
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto, FAQ, Rating, Article,
    District, MetroStation, City, Gruzovoy, Manipulyator, Highway, Region,
    AboutPage, ArticlePage, PricePage, GalleryPage, CalculatorPage,
)

import requests
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt  # если хочешь, но лучше убрать и использовать token в форме

TELEGRAM_TOKEN = "1625085576:AAGR1VzsLToXxe5NxiPGA-IZy1NmQlbNX7U"  # или хранить в settings.SECRET
TELEGRAM_CHAT_ID = "-1003511742071"
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
        return JsonResponse({"success": False, "message": "Не удалось отправить сообщение."})


@csrf_exempt
def send_callback(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Только POST"}, status=400)

    name = request.POST.get("name", "").strip() or "Не указано"
    phone = request.POST.get("phone", "").strip()
    agree = request.POST.get("agree_policy", "false")

    if not phone:
        return JsonResponse({"success": False, "message": "Укажите телефон"})

    message = (
        "НОВАЯ ЗАЯВКА\n\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Согласен с политикой: {agree}"
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

def policy(request):
    return render(request, 'policy.html')

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

    
   
    context = {
        'hero': hero,
        'order_steps': order_steps,
        'transports': transports,
        'info': info,
        'prices': prices,
        'why_choose_us': why_choose_us,
        'photos': photos,
        'faqs': faqs,
    }
    return render(request, 'index.html', context)

# ДЕТАЛЬНАЯ СТРАНИЦА — РАБОТАЕТ СРАЗУ
def transport_detail(request, slug):
    transport = get_object_or_404(TransportType, slug=slug)
    
    context = {
        'transport': transport,
        'gallery': transport.gallery.all()[:12],           # фотки из галереи
        'prices': PriceItem.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True)[:10],
    }
    return render(request, 'transport_detail.html', context)


def services(request):
    return render(request, 'services.html')

def district_list(request):
    districts = District.objects.all()
    return render(request, 'district_list.html', {'districts': districts})


def metro_list(request):
    stations = MetroStation.objects.select_related('district').all()
    return render(request, 'metro_list.html', {'stations': stations})

# Грузовой
def gruzovoy_detail(request, slug):
    item = get_object_or_404(Gruzovoy, slug=slug)
    return render(request, 'metro_list.html', {'item': item})

# Манипулятор
def manipulyator_detail(request, slug):
    item = get_object_or_404(Manipulyator, slug=slug)
    return render(request, 'metro_list.html', {'item': item})

# Шоссе
def highway_detail(request, slug):
    item = get_object_or_404(Highway, slug=slug)
    return render(request, 'metro_list.html', {'item': item})

def location_detail(request, slug):
    location = None
    location_type = None

    if District.objects.filter(slug=slug).exists():
        location = get_object_or_404(District, slug=slug)
        location_type = 'district'
    elif Region.objects.filter(slug=slug).exists():
        location = get_object_or_404(Region, slug=slug)
        location_type = 'oblasti'
    elif MetroStation.objects.filter(slug=slug).exists():
        location = get_object_or_404(MetroStation, slug=slug)
        location_type = 'metro'
    elif City.objects.filter(slug=slug).exists():
        location = get_object_or_404(City, slug=slug)
        location_type = 'city'
    elif Gruzovoy.objects.filter(slug=slug).exists():
        location = get_object_or_404(Gruzovoy, slug=slug)
        location_type = 'gruzovoy'
    elif Manipulyator.objects.filter(slug=slug).exists():
        location = get_object_or_404(Manipulyator, slug=slug)
        location_type = 'manipulyator'
    elif Highway.objects.filter(slug=slug).exists():
        location = get_object_or_404(Highway, slug=slug)
        location_type = 'highway'
    else:
        raise Http404("Страница не найдена")

    context = {
        'location': location,
        'location_type': location_type,
        'order_steps': HowToOrderStep.objects.all(),
        'transports': TransportType.objects.all(),
        'info': InfoSection.objects.first(),
        'prices': PriceItem.objects.all(),
        'why_choose_us': WhyChooseUs.objects.all(),
        'photos': WorkPhoto.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True)[:6],
       
    }
    return render(request, 'location_detail.html', context)

def payment(request):
    return render(request, 'payment.html')

def about(request):
    info = InfoSection.objects.first()
    photos = WorkPhoto.objects.all()
    aboutpage = AboutPage.objects.first()

    context = {
        'info': info,
        'page_info': aboutpage,
        'photos': photos,
        'order_steps': HowToOrderStep.objects.all(),
        'why_choose_us': WhyChooseUs.objects.all(),
    }

    return render(request, 'about.html', context)
 

def article_list(request):
    articles = Article.objects.all()
    articlepage = ArticlePage.objects.first()

    context = {
        "articles": articles,
        "page_info": articlepage, 
    }
    return render(request, 'articles.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})

def prices(request):
    prices = PriceItem.objects.all()
    pricepage = PricePage.objects.first()

    context = {
        "prices": prices,
        "page_info": pricepage,
    }

    return render(request, 'prices.html', context)

def gallery(request):
    photos = WorkPhoto.objects.all()
    gallerypage = GalleryPage.objects.first()

    context = {
        "photos": photos,
        "page_info": gallerypage, 
    }

    return render(request, 'gallery.html', context)

def calculator(request):
    calculatorpage = CalculatorPage.objects.first()

    context = {
        "page_info": calculatorpage,
    }
    return render(request, 'calculator.html', context)


def oplata(request):
    return render(request, 'oplata.html')


from .models import Page


def home(request):
    page = get_object_or_404(Page, is_active=True)
    
    
    context = {
        'page': page,
        # Все связи уже доступны через page.название_связи.all()
        'hero_sections': page.hero_sections.all(),
        'how_to_order_steps': page.how_to_order_steps.all().order_by('order'),
        'transport_types': page.transport_types.all(),
        'why_choose_us': page.why_choose_us.all(),
        'calculator': page.calculator,
        'info_sections': page.info_sections.all(),
        'price_items': page.price_items.all(),
        'work_photos': page.work_photos.all(),
        'faqs': page.faqs.filter(is_active=True),
        'ratings': page.ratings.all(),
        'articles': page.articles.all().order_by('-date')[:5],
        'cities': page.cities.all(),
        'metro_stations': page.metro_stations.all(),
        'regions': page.regions.all(),
        'districts': page.districts.all(),
        'gruzovoys': page.gruzovoys.all(),
        'manipulyators': page.manipulyators.all(),
        'highways': page.highways.all(),
    }
    
    return render(request, 'page_detail.html', context)


def page_detail(request, slug=None):
    if slug:
        # Для обычных страниц - ищем по slug
        try:
            page = Page.objects.get(slug=slug, is_active=True, is_homepage=False)
        except Page.DoesNotExist:
            raise Http404("Страница не найдена")
        except Page.MultipleObjectsReturned:
            # Если несколько страниц с одинаковым slug, берем первую
            page = Page.objects.filter(slug=slug, is_active=True, is_homepage=False).first()
    else:
        # Для главной страницы - ищем где is_homepage=True
        try:
            page = Page.objects.get(is_homepage=True, is_active=True)
        except Page.DoesNotExist:
            # Если нет главной, создаем ее или используем первую активную
            page = Page.objects.filter(is_active=True).first()
            if not page:
                raise Http404("Нет активных страниц")
        except Page.MultipleObjectsReturned:
            # Если несколько главных страниц, берем первую
            page = Page.objects.filter(is_homepage=True, is_active=True).first()
    
    context = {
        'page': page,
        # Все связи уже доступны через page.название_связи.all()
        'hero_sections': page.hero_sections.all(),
        'how_to_order_steps': page.how_to_order_steps.all().order_by('order'),
        'transport_types': page.transport_types.all(),
        'why_choose_us': page.why_choose_us.all(),
        'calculator': page.calculator,
        'payment': page.payment_show,
        'second_hero_section': page.second_hero_section,
        'fastorder': page.fastorder,
        'question_map': page.question_map,
        'map_show': page.map_show,
        'info_sections': page.info_sections.all(),
        'price_items': page.price_items.all(),
        'work_photos': page.work_photos.all(),
        'faqs': page.faqs.filter(is_active=True),
        'ratings': page.ratings.all(),
        'articles': page.articles.all().order_by('-date')[:5],
        'cities': page.cities.all(),
        'metro_stations': page.metro_stations.all(),
        'regions': page.regions.all(),
        'districts': page.districts.all(),
        'gruzovoys': page.gruzovoys.all(),
        'manipulyators': page.manipulyators.all(),
        'highways': page.highways.all(),
    }
    
    return render(request, 'page_detail.html', context)
