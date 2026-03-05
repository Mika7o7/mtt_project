from django.db import models


# ===== HERO =====
class HeroSection(models.Model):
    title = models.CharField("Главный заголовок", max_length=255)
    subtitle = models.TextField("Подзаголовок", blank=True)
    button_text = models.CharField("Текст кнопки", max_length=100, default="Заказать звонок")
    model_3d = models.FileField("3D модель", upload_to="models/", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Секция Hero"
        verbose_name_plural = "Секции Hero"


# ===== HOW TO ORDER =====
class HowToOrderStep(models.Model):
    icon = models.CharField("Иконка (эмодзи или HTML)", max_length=10)
    title = models.CharField("Заголовок", max_length=100)
    description = models.CharField("Описание", max_length=255)
    image = models.ImageField("Картинка", upload_to="how_to_order/")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Шаг 'Как заказать'"
        verbose_name_plural = "Шаги 'Как заказать'"

    def __str__(self):
        return f"{self.order}. {self.title}"


class TransportType(models.Model):
    name = models.CharField("Название типа", max_length=100)
    slug = models.SlugField(
        "ЧПУ (например: legkovye)", 
        max_length=100, 
        blank=True,      # ← обязательно!
        null=True,       # ← обязательно!
        unique=True      # ← можно оставить, НО только с blank=True, null=True
    )
    image = models.ImageField("Главное фото", upload_to="transport/")
    description = models.TextField("Полное описание", blank=True)
    icon = models.ImageField("Иконка", upload_to="transport/icons/", blank=True, null=True)
    button_text = models.CharField("Текст кнопки", max_length=50, default="Заказать эвакуатор")
    gallery = models.ManyToManyField('WorkPhoto', blank=True, related_name='transport_gallery')
    price_from = models.DecimalField("Цена от", max_digits=8, decimal_places=0, default=2500)
    features = models.TextField("Особенности", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип транспорта"
        verbose_name_plural = "Типы транспорта"


# ===== WHY CHOOSE US =====
class WhyChooseUs(models.Model):
    icon = models.CharField("Иконка (эмодзи)", max_length=10)
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Почему выбрать нас"
        verbose_name_plural = "Почему выбрать нас"


# ===== INFO SECTION (ТЕКСТ + КАРТИНКА) =====
class InfoSection(models.Model):
    image = models.ImageField("Фото", upload_to="info/")
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    button_text = models.CharField("Текст кнопки", max_length=50, default="Связаться с нами")
    # button_link = models.URLField("Ссылка кнопки", default="#", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Секция Информация"
        verbose_name_plural = "Секции Информация"


# ===== PRICE LIST =====
class PriceItem(models.Model):
    title = models.CharField("Название услуги", max_length=255)
    price = models.CharField("Цена", max_length=50)

    def __str__(self):
        return f"{self.title} — {self.price}"

    class Meta:
        verbose_name = "Элемент прайс-листа"
        verbose_name_plural = "Прайс-лист"


# ===== PHOTO GALLERY =====
class WorkPhoto(models.Model):
    image = models.ImageField("Фото", upload_to="works/")
    caption = models.CharField("Описание", max_length=100, blank=True)

    def __str__(self):
        return self.caption or f"Фото {self.id}"

    class Meta:
        verbose_name = "Фото работы"
        verbose_name_plural = "Фото работы"


# ===== FAQ =====
class FAQ(models.Model):
    question = models.CharField("Вопрос", max_length=255)
    answer = models.TextField("Ответ")
    is_active = models.BooleanField("Показывать", default=False)  # новое поле

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "FAQ"


# ===== ARTICLE =====
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title
    



class Page(models.Model):
    PAGE_TYPE_CHOICES = (
        ('default',        'Обычная страница'),
        ('metro',          'Метро'),
        ('district',       'Районы'),
        ('region',         'Области'),
        ('highway',        'Шоссе'),
        ('service',        'Услуга'),
        ('evacuator_city_mo', 'Эвакуатор по городам МО'),   # ← новый тип
    )
    
    page_type = models.CharField(
        "Тип страницы",
        max_length=20,
        choices=PAGE_TYPE_CHOICES,
        default='default',
        db_index=True
    )
    name = models.CharField("Название страницы", max_length=150)
    slug = models.CharField(
        "URL страницы",
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text="Оставьте пустым для главной страницы. Можно использовать слеши (/) для вложенных URL"
    )
    is_homepage = models.BooleanField("Главная страница", default=False)
    
    # SEO поля
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True)
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)
    
    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова", blank=True)
    
    # Связи с существующими моделями
    hero_sections = models.ManyToManyField(
        'HeroSection', 
        blank=True, 
        verbose_name="Hero секции",
        related_name='pages'
    )
    
    how_to_order_steps = models.ManyToManyField(
        'HowToOrderStep', 
        blank=True, 
        verbose_name="Шаги 'Как заказать'",
        related_name='pages'
    )
    
    transport_types = models.ManyToManyField(
        'TransportType', 
        blank=True, 
        verbose_name="Типы транспорта",
        related_name='pages'
    )
    
    why_choose_us = models.ManyToManyField(
        'WhyChooseUs', 
        blank=True, 
        verbose_name="Почему выбрать нас",
        related_name='pages'
    )
    
    fastorder = models.BooleanField("показать Срочный заказ эвакуатора", default=False)
    calculator = models.BooleanField("показать калькулятор", default=False)
    question_map = models.BooleanField("показать Остались вопросы", default=False)
    map_show = models.BooleanField("показать картy", default=False)
    payment_show = models.BooleanField("показать qr", default=False)
    second_hero_section = models.BooleanField("показать второй тип hero section", default=False)
    
    info_sections = models.ManyToManyField(
        'InfoSection', 
        blank=True, 
        verbose_name="Инфо секции",
        related_name='pages'
    )
    
    price_items = models.ManyToManyField(
        'PriceItem', 
        blank=True, 
        verbose_name="Прайс-лист",
        related_name='pages'
    )
    
    work_photos = models.ManyToManyField(
        'WorkPhoto', 
        blank=True, 
        verbose_name="Фото работ",
        related_name='pages'
    )
    
    faqs = models.ManyToManyField(
        'FAQ', 
        blank=True, 
        verbose_name="FAQ",
        related_name='pages'
    )
    
    articles = models.ManyToManyField(
        'Article', 
        blank=True, 
        verbose_name="Статьи",
        related_name='pages'
    )
    
    # Настройки
    is_active = models.BooleanField("Активная страница", default=True)
    order = models.PositiveIntegerField("Порядок в меню", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.is_homepage:
            return '/'
        return f'/{self.slug}/'

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Проверка, что только одна страница может быть главной
        if self.is_homepage:
            if Page.objects.filter(is_homepage=True).exclude(id=self.id).exists():
                raise ValidationError('Может быть только одна главная страница')
        
        # Если это главная страница, слаг должен быть пустым
        if self.is_homepage and self.slug:
            raise ValidationError('Главная страница не должна иметь slug')
        
        # Если не главная, слаг обязателен
        if not self.is_homepage and not self.slug:
            raise ValidationError('Обычные страницы должны иметь slug')