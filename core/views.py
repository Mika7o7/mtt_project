import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt  # если хочешь, но лучше убрать и использовать token в форме

from .models import TransportType, PriceItem, FAQ, Article, Page
    

TELEGRAM_TOKEN = "1625085576:AAGR1VzsLToXxe5NxiPGA-IZy1NmQlbNX7U"  # или хранить в settings.SECRET
TELEGRAM_CHAT_ID = "-1003511742071"

@csrf_exempt
def universal_form(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Некорректный запрос"},
            status=400
        )

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
        'articles': page.articles.all().order_by('-date')[:5],
        # Удаленные поля убраны
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
        'articles': page.articles.all().order_by('-date')[:5],
        # Удаленные поля убраны
    }
    
    return render(request, 'page_detail.html', context)