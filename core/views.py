import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt  # если хочешь, но лучше убрать и использовать token в форме
from django.conf import settings

from .models import TransportType, PriceItem, FAQ, Article, Page, CalculatorVehicleType, CalculatorCategory, CalculatorExtraService
    

TELEGRAM_TOKEN = "1625085576:AAGR1VzsLToXxe5NxiPGA-IZy1NmQlbNX7U"  # или хранить в settings.SECRET
TELEGRAM_CHAT_ID = "-1003511742071"

def verify_recaptcha(token):
   

    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.post(url, data=data, headers=headers, timeout=5)
        result = r.json()
        print("=== Google reCAPTCHA response ===")
        print(result)
        return result.get('success', False) and result.get('score', 0) >= settings.RECAPTCHA_MIN_SCORE
    except Exception as e:
        print("Exception in verify_recaptcha:", e)
        return False

@csrf_exempt
def universal_form(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Некорректный запрос"},
            status=400
        )

    # Перевірка reCAPTCHA
    recaptcha_token = request.POST.get('g-recaptcha-response')
    print("Received token:", recaptcha_token)
    if not recaptcha_token or not verify_recaptcha(recaptcha_token):
        return JsonResponse({'success': False, 'message': 'Проверка reCAPTCHA не пройдена. Попробуйте ещё раз.'})


    form_type = request.POST.get("form_type", "").strip()

    # =========================
    # FASTORDER
    # =========================
    if form_type == "fastorder":
        name = request.POST.get("f_name", "").strip() or "Не указано"
        phone = request.POST.get("f_phone", "").strip()
        avto = request.POST.get("f_ztxt", "").strip()

        if not phone:
            return JsonResponse({"success": False, "message": "Укажите телефон"})

        message = (
            "📞 <b>Заказать звонок</b>\n\n"
            f"👤 Имя: {name}\n"
            f"📞 Телефон: {phone}\n"
            f"✅ Авто: {avto}"
        )

    # =========================
    # CALLBACK
    # =========================
    elif form_type == "callback":
        name = request.POST.get("name", "").strip() or "Не указано"
        phone = request.POST.get("phone", "").strip()
        agree = request.POST.get("agree_policy", "false")

        if not phone:
            return JsonResponse({"success": False, "message": "Укажите телефон"})

        message = (
            "📞 <b>Заказать звонок</b>\n\n"
            f"👤 Имя: {name}\n"
            f"📞 Телефон: {phone}\n"
            f"✅ Согласие с политикой: {agree}"
        )

    # =========================
    # QUESTION
    # =========================
    elif form_type == "question":
        name = request.POST.get("q_name", "").strip()
        phone = request.POST.get("q_phone", "").strip()
        question = request.POST.get("q_question", "").strip()

        if not phone:
            return JsonResponse({"success": False, "message": "Укажите телефон"})

        message = (
            "❓ <b>Вопрос с сайта</b>\n\n"
            f"👤 Имя: {name or '—'}\n"
            f"📞 Телефон: {phone}\n"
        )

        if question:
            message += f"📝 Вопрос: {question}\n"

    # =========================
    # CALCULATOR (submit_form)
    # =========================
    elif form_type == "calculator":
        # --- Основные поля ---
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

        if not phone:
            return JsonResponse({"success": False, "message": "Укажите номер телефона."})

        # --- Типы авто ---
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

        # --- Доп. опции ---
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

        extras = [
            label for key, label in dop_map.items()
            if request.POST.get(key) == "1"
        ]
        extras_text = ", ".join(extras) if extras else "—"

        message = (
            "🚨 <b>Новая заявка эвакуатор</b>\n\n"
            f"👤 Имя: {name or '—'}\n"
            f"📞 Телефон: {phone}\n"
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

    else:
        return JsonResponse(
            {"success": False, "message": "Неизвестный тип формы"}
        )

    # =========================
    # SEND TO TELEGRAM
    # =========================
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=5,
        )
        r.raise_for_status()

    except Exception as e:
        print("Ошибка Telegram:", e)
        return JsonResponse(
            {"success": False, "message": "Не удалось отправить сообщение."}
        )

    return JsonResponse(
        {"success": True, "message": "Спасибо! Заявка успешно отправлена."}
    )

def policy(request):
    return render(request, 'policy.html')


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



def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})




def home(request):
    page = get_object_or_404(Page, is_active=True, is_homepage=True)
    
    # Получаем данные для калькулятора из админки (убираем is_active)
    calculator_vehicle_types = CalculatorVehicleType.objects.filter(
        vehicle_type='evacuator'
    ).order_by('order', 'name')  # ← сортировка по order
    
    calculator_manipulator_types = CalculatorVehicleType.objects.filter(
        vehicle_type='manipulator'
    ).order_by('order', 'name')
    
    # Группируем категории по типу транспорта
    evacuator_categories_by_type = {}
    for vt in calculator_vehicle_types:
        evacuator_categories_by_type[vt.id] = list(vt.categories.all().order_by('order', 'name'))
    
    manipulator_categories_by_type = {}
    for vt in calculator_manipulator_types:
        manipulator_categories_by_type[vt.id] = vt.categories.all().order_by('order', 'name')
    
    # Получаем дополнительные услуги
    evacuator_extra_services = CalculatorExtraService.objects.filter(
        vehicle_type='evacuator'
    ).order_by('order', 'name')
    
    manipulator_extra_services = CalculatorExtraService.objects.filter(
        vehicle_type='manipulator'
    ).order_by('order', 'name')
    
    context = {
        'page': page,
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
        'articles': page.articles.all().order_by('-date')[:5],
        # Данные для калькулятора
        'calculator_vehicle_types': calculator_vehicle_types,
        'calculator_manipulator_types': calculator_manipulator_types,
        'evacuator_categories_by_type': evacuator_categories_by_type,
        'manipulator_categories_by_type': manipulator_categories_by_type,
        'evacuator_extra_services': evacuator_extra_services,
        'manipulator_extra_services': manipulator_extra_services,
    }
    
    return render(request, 'page_detail.html', context)



def page_detail(request, path=None):
    """
    Универсальный view для всех страниц
    """
    if path is None:
        page = get_object_or_404(Page, is_homepage=True, is_active=True)
    else:
        try:
            page = Page.objects.get(slug=path, is_active=True)
        except Page.DoesNotExist:
            last_part = path.split('/')[-1]
            page = get_object_or_404(Page, slug=last_part, is_active=True)
        except Page.MultipleObjectsReturned:
            page = Page.objects.filter(slug=path, is_active=True).first()
    
    # Получаем данные для калькулятора из админки (убираем is_active)
    calculator_vehicle_types = CalculatorVehicleType.objects.filter(
        vehicle_type='evacuator'
    ).order_by('order', 'name')  # ← сортировка по order
    
    calculator_manipulator_types = CalculatorVehicleType.objects.filter(
        vehicle_type='manipulator'
    ).order_by('order', 'name')
    
    # Группируем категории с сортировкой
    evacuator_categories_by_type = {}
    for vt in calculator_vehicle_types:
        evacuator_categories_by_type[vt.id] = vt.categories.all().order_by('order', 'name')
    
    manipulator_categories_by_type = {}
    for vt in calculator_manipulator_types:
        manipulator_categories_by_type[vt.id] = vt.categories.all().order_by('order', 'name')
    
    # Дополнительные услуги с сортировкой (убираем is_active)
    evacuator_extra_services = CalculatorExtraService.objects.filter(
        vehicle_type='evacuator'
    ).order_by('order', 'name')
    
    manipulator_extra_services = CalculatorExtraService.objects.filter(
        vehicle_type='manipulator'
    ).order_by('order', 'name')
    
    context = {
        'page': page,
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
        'articles': page.articles.all().order_by('-date')[:5],
        # Данные для калькулятора
        'calculator_vehicle_types': calculator_vehicle_types,
        'calculator_manipulator_types': calculator_manipulator_types,
        'evacuator_categories_by_type': evacuator_categories_by_type,
        'manipulator_categories_by_type': manipulator_categories_by_type,
        'evacuator_extra_services': evacuator_extra_services,
        'manipulator_extra_services': manipulator_extra_services,
    }
    
    return render(request, 'page_detail.html', context)