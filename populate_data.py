from django.utils.text import slugify
from core.models import MetaData, HeroSection, District, OrderStep, FormConfig, VideoReview, Photo, Price, Service, WhyChooseUs, FAQ, Rating, CalculatorOption

# MetaData
MetaData.objects.create(
    page='moscow_services',
    title='Вызвать эвакуатор в Москве недорого – заказать круглосуточные услуги по доступной цене',
    keywords='эвакуатор москва, вызвать эвакуатор, эвакуатор круглосуточно, эвакуатор недорого, доступная цена эвакуатора, эвакуация москва, служба эвакуации, эвакуатор 24/7',
    description='Вызвать эвакуатор в Москве круглосуточно по доступной цене – это просто! Наша служба эвакуации обеспечивает оперативную помощь 24/7, с оплатой картой или по QR-коду и с онлайн-расчетом стоимости. Мы предоставляем надежное и недорогое обслуживание в любых дорожных ситуациях.',
    og_url='https://evacuator-avto.ru',
    og_title='Вызвать эвакуатор в Москве недорого – заказать круглосуточные услуги по доступной цене',
    og_image='og_images/og_image.png',  # Замените на реальный путь к файлу
    og_description='Вызвать эвакуатор в Москве круглосуточно по доступной цене – это просто! Наша служба эвакуации обеспечивает оперативную помощь 24/7, с оплатой картой или по QR-коду и с онлайн-расчетом стоимости. Мы предоставляем надежное и недорогое обслуживание в любых дорожных ситуациях.',
    canonical_url_name='moscow_services'
)

# HeroSection
HeroSection.objects.create(
    page='moscow_services',
    title='Эвакуатор в Москве',
    description='Круглосуточные услуги эвакуации автомобилей быстро и недорого.<br>Подача эвакуатора в течение 18 минут. Безопасная транспортировка<br>вашего автомобиля, внимание каждому клиенту и его<br> потребностям.',
    background_image='hero_images/bg.jpg',  # Замените на реальный путь к файлу
    low_price=3800.00,
    price_currency='RUB',
    availability_url='http://schema.org/InStock',
    url_name='moscow_services'
)

# Districts
districts_data = [
    {'name': 'По округам Москвы', 'url_name': 'districts'},
    {'name': 'Эвакуатор возле метро', 'url_name': 'metro'},
    {'name': 'Эвакуатор по районам Москвы', 'url_name': 'districts'},
    {'name': 'Эвакуатор Зеленоград', 'url_name': 'zelenograd'},
    {'name': 'Эвакуатор Новомосковский', 'url_name': 'novomoskovskiy'},
    {'name': 'Эвакуатор Троицк', 'url_name': 'troick'},
]
for data in districts_data:
    slug = slugify(data['name'])
    if not District.objects.filter(slug=slug).exists():
        District.objects.create(
            name=data['name'],
            slug=slug,
            url_name=data['url_name']
        )

# OrderStep
OrderStep.objects.create(
    title='Связаться с нами',
    description='Оформить заказ на эвакуацию возможно как по телефону, так и онлайн, через специальную форму на сайте',
    icon='order_icons/kak_1.svg',  # Замените на реальный путь к файлу
    number_icon='order_number_icons/t1.svg',  # Замените на реальный путь к файлу
    order=1
)
# TODO: Добавьте еще 3 объекта OrderStep для остальных шагов

# FormConfig
FormConfig.objects.create(
    form_id='form_1',
    title='Просто оставьте заявку,<br> а в остальном <span class="g-color-primary">мы поможем</span>',
    f_vid='2',
    page_id='7',
    dop_id='0',
    background_image='form_bg/2.jpg'  # Замените на реальный путь к файлу
)
FormConfig.objects.create(
    form_id='form_2',
    title='Обслуживание 24 часа',
    f_vid='3',
    page_id='7',
    dop_id='0',
    background_image='form_bg/3.jpg'  # Замените на реальный путь к файлу
)
FormConfig.objects.create(
    form_id='urgent_form',
    title='Срочный заказ эвакуатора',
    f_vid='4',
    page_id='7',
    dop_id='0',
    background_image='form_bg/1.jpg'  # Замените на реальный путь к файлу
)

# VideoReview
VideoReview.objects.create(
    title='Видеоотзыв клиента Nissan Teana',
    youtube_url='https://youtu.be/073Syahnoog',
    thumbnail='video_thumbnails/5.jpg',  # Замените на реальный путь к файлу
    order=1
)
# TODO: Добавьте еще 7 объектов VideoReview

# Photo
Photo.objects.create(
    image='gallery/136.jpg',  # Замените на реальный путь к файлу
    thumbnail='gallery_thumbnails/sm/136.jpg',  # Замените на реальный путь к файлу
    caption='фото',
    order=1
)
# TODO: Добавьте еще объекты Photo

# Price
Price.objects.create(
    service='Эвакуатор для мотоциклов',
    price='от 4000 р.'
)
# TODO: Добавьте еще объекты Price

# Service
Service.objects.create(
    title='Вызвать эвакуатор в Москве',
    description='Эвакуатор в Москве — оперативная помощь на дороге в любое время суток! ...',
    image='service_images/sm/251.jpg',  # Замените на реальный путь к файлу
    url_name='moscow_services'
)
Service.objects.create(
    title='Эвакуатор в Москве — Быстрый расчёт и прозрачные условия',
    description='EVACUATOR-AVTO.RU — ваш надёжный партнёр в Москве, срочная эвакуация автомобиля. ...',
    image='service_images/sm/127.jpg',  # Замените на реальный путь к файлу
    url_name='moscow_services'
)

# WhyChooseUs
WhyChooseUs.objects.create(
    title='Все документы для страховой компании',
    description='Заказывая эвакуатор у нас, вы можете быть уверены, что получите все необходимые документы',
    icon='why_choose_us_icons/why_1.svg',  # Замените на реальный путь к файлу
    order=1
)
# TODO: Добавьте еще 3 объекта WhyChooseUs

# FAQ
FAQ.objects.create(
    question='Как заказать эвакуатор в Москве?',
    answer='Чтобы заказать эвакуатор позвоните по номеру <a href="tel:+74955131347" class="u-link-v1 g-nowrap g-font-size-16 g-font-weight-700">+7 (495) 513-13-47</a> или воспользуйтесь онлайн-заказом на нашем сайте.',
    order=1
)
# TODO: Добавьте еще 5 объектов FAQ

# Rating
Rating.objects.create(
    page='moscow_services',
    rating_value=4.9,
    review_count=137,
    item_reviewed='Услуги авто эвакуатора',
    worst_rating=1
)

# CalculatorOption
CalculatorOption.objects.create(
    option_type='vehicle_type',
    name='Седан',
    value='1',
    discount='5'
)
# TODO: Добавьте еще объекты CalculatorOption