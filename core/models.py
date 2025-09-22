from django.db import models
from django.utils.text import slugify


class MetaData(models.Model):
    """
    Stores metadata for SEO (title, keywords, description, OG tags).
    """
    page = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="Unique identifier for the page (e.g., 'moscow_services')",
        verbose_name="Страница"
    )
    title = models.CharField(
        max_length=255, 
        help_text="Page title for SEO",
        verbose_name="Заголовок страницы"
    )
    keywords = models.TextField(
        blank=True, 
        help_text="Comma-separated keywords for SEO",
        verbose_name="Ключевые слова"
    )
    description = models.TextField(
        blank=True, 
        help_text="Page description for SEO",
        verbose_name="Описание"
    )
    og_url = models.URLField(
        blank=True, 
        help_text="Open Graph URL",
        verbose_name="OG URL"
    )
    og_title = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Open Graph title",
        verbose_name="OG Заголовок"
    )
    og_image = models.ImageField(
        upload_to='og_images/', 
        blank=True, 
        help_text="Open Graph image",
        verbose_name="OG Изображение"
    )
    og_description = models.TextField(
        blank=True, 
        help_text="Open Graph description",
        verbose_name="OG Описание"
    )
    canonical_url_name = models.CharField(
        max_length=255, 
        help_text="Django URL name for canonical link (e.g., 'moscow_services')",
        verbose_name="Имя URL для канонической ссылки"
    )

    def __str__(self):
        return self.page

    class Meta:
        verbose_name = "Мета-данные"
        verbose_name_plural = "Мета-данные"


class HeroSection(models.Model):
    """
    Stores data for the Hero Section (title, description, offer details).
    """
    page = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="Page identifier (e.g., 'moscow_services')",
        verbose_name="Страница"
    )
    title = models.CharField(
        max_length=255, 
        help_text="Main heading (e.g., 'Эвакуатор в Москве')",
        verbose_name="Заголовок"
    )
    description = models.TextField(
        help_text="Description text for the hero section",
        verbose_name="Описание"
    )
    background_image = models.ImageField(
        upload_to='hero_images/', 
        blank=True, 
        help_text="Background image for the hero section",
        verbose_name="Фоновое изображение"
    )
    low_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Lowest price for the offer",
        verbose_name="Минимальная цена"
    )
    price_currency = models.CharField(
        max_length=3, 
        default="RUB", 
        help_text="Currency code (e.g., 'RUB')",
        verbose_name="Валюта"
    )
    availability_url = models.URLField(
        blank=True, 
        help_text="Schema.org availability URL (e.g., 'http://schema.org/InStock')",
        verbose_name="URL доступности"
    )
    url_name = models.CharField(
        max_length=255, 
        help_text="Django URL name for the offer link",
        verbose_name="Имя URL для ссылки"
    )

    class Meta:
        verbose_name = "Секция Hero"
        verbose_name_plural = "Секции Hero"

    def __str__(self):
        return self.title



class District(models.Model):
    """
    Stores data for districts and areas (e.g., Zelenograd, Novomoskovskiy).
    """
    name = models.CharField(
        max_length=255, 
        help_text="District or area name (e.g., 'Зеленоград')",
        verbose_name="Название района"
    )
    slug = models.SlugField(
        unique=True, 
        blank=True, 
        help_text="URL-friendly slug",
        verbose_name="Слаг"
    )
    url_name = models.CharField(
        max_length=255, 
        help_text="Django URL name (e.g., 'zelenograd')",
        verbose_name="Имя URL"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"

    def __str__(self):
        return self.name



class OrderStep(models.Model):
    """
    Stores steps for the 'How to Order' section.
    """
    title = models.CharField(
        max_length=255, 
        help_text="Step title (e.g., 'Связаться с нами')",
        verbose_name="Заголовок шага"
    )
    description = models.TextField(
        help_text="Step description",
        verbose_name="Описание шага"
    )
    icon = models.FileField(
        upload_to='order_icons/', 
        blank=True, 
        help_text="Icon for the step",
        verbose_name="Иконка шага"
    )
    number_icon = models.FileField(
        upload_to='order_number_icons/', 
        blank=True, 
        help_text="Number icon for the step",
        verbose_name="Номерная иконка"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Order of the step in the carousel",
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Шаг заказа"
        verbose_name_plural = "Шаги заказа"

    def __str__(self):
        return self.title


class FormConfig(models.Model):
    """
    Stores configuration for form sections (e.g., hidden inputs, titles).
    """
    form_id = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="Unique form identifier (e.g., 'form_1')",
        verbose_name="Идентификатор формы"
    )
    title = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Form title (e.g., 'Просто оставьте заявку')",
        verbose_name="Заголовок формы"
    )
    f_vid = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Hidden field 'f_vid' value",
        verbose_name="f_vid"
    )
    page_id = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Hidden field 'page_id' value",
        verbose_name="page_id"
    )
    dop_id = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Hidden field 'dop_id' value",
        verbose_name="dop_id"
    )
    background_image = models.ImageField(
        upload_to='form_bg/', 
        blank=True, 
        help_text="Background image for the form section",
        verbose_name="Фоновое изображение"
    )

    def __str__(self):
        return self.form_id

    class Meta:
        verbose_name = "Конфигурация формы"
        verbose_name_plural = "Конфигурации форм"


class VideoReview(models.Model):
    """
    Stores video reviews (YouTube links and descriptions).
    """
    title = models.CharField(
        max_length=255, 
        help_text="Review title (e.g., 'Видеоотзыв клиента Nissan Teana')",
        verbose_name="Заголовок отзыва"
    )
    youtube_url = models.URLField(
        help_text="YouTube video URL",
        verbose_name="URL видео"
    )
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/', 
        blank=True, 
        help_text="Thumbnail image for the video",
        verbose_name="Миниатюра"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Order in the carousel",
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Видеоотзыв"
        verbose_name_plural = "Видеоотзывы"

    def __str__(self):
        return self.title


class Photo(models.Model):
    """
    Stores photos for the gallery section.
    """
    image = models.ImageField(
        upload_to='gallery/', 
        help_text="Photo for the gallery",
        verbose_name="Изображение"
    )
    thumbnail = models.ImageField(
        upload_to='gallery_thumbnails/', 
        blank=True, 
        help_text="Thumbnail for the photo",
        verbose_name="Миниатюра"
    )
    caption = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Photo caption",
        verbose_name="Подпись"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Order in the gallery",
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Фото"
        verbose_name_plural = "Фотогалерея"

    def __str__(self):
        return self.caption or f"Photo {self.id}"


class Price(models.Model):
    """
    Stores pricing data for the price table.
    """
    service = models.CharField(
        max_length=255, 
        help_text="Service name (e.g., 'Эвакуатор для мотоциклов')",
        verbose_name="Услуга"
    )
    price = models.CharField(
        max_length=50, 
        help_text="Price (e.g., 'от 4000 р.')",
        verbose_name="Цена"
    )

    def __str__(self):
        return f"{self.service} - {self.price}"

    class Meta:
        verbose_name = "Цена услуги"
        verbose_name_plural = "Прайс-лист"


class Service(models.Model):
    """
    Stores service descriptions and associated images.
    """
    title = models.CharField(
        max_length=255, 
        help_text="Service title (e.g., 'Вызвать эвакуатор в Москве')",
        verbose_name="Заголовок услуги"
    )
    description = models.TextField(
        help_text="Service description",
        verbose_name="Описание услуги"
    )
    image = models.ImageField(
        upload_to='service_images/', 
        blank=True, 
        help_text="Image for the service",
        verbose_name="Изображение"
    )
    url_name = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Django URL name for the service",
        verbose_name="Имя URL"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class WhyChooseUs(models.Model):
    """
    Stores reasons for the 'Why Choose Us' section.
    """
    title = models.CharField(
        max_length=255, 
        help_text="Reason title (e.g., 'Все документы для страховой компании')",
        verbose_name="Заголовок преимущества"
    )
    description = models.TextField(
        help_text="Reason description",
        verbose_name="Описание преимущества"
    )
    icon = models.ImageField(
        upload_to='why_choose_us_icons/', 
        blank=True, 
        help_text="Icon for the reason",
        verbose_name="Иконка"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Order in the section",
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """
    Stores FAQ questions and answers.
    """
    question = models.CharField(
        max_length=255, 
        help_text="Question text",
        verbose_name="Вопрос"
    )
    answer = models.TextField(
        help_text="Answer text",
        verbose_name="Ответ"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Order in the FAQ section",
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "Вопросы FAQ"

    def __str__(self):
        return self.question


class Rating(models.Model):
    """
    Stores rating data for the rating section.
    """
    page = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="Page identifier (e.g., 'moscow_services')",
        verbose_name="Страница"
    )
    rating_value = models.FloatField(
        default=0.0, 
        help_text="Average rating (e.g., 4.9)",
        verbose_name="Средний рейтинг"
    )
    review_count = models.PositiveIntegerField(
        default=0, 
        help_text="Number of reviews (e.g., 137)",
        verbose_name="Количество отзывов"
    )
    item_reviewed = models.CharField(
        max_length=255, 
        help_text="Item reviewed (e.g., 'Услуги авто эвакуатора')",
        verbose_name="Отзыв о"
    )
    worst_rating = models.PositiveIntegerField(
        default=1, 
        help_text="Worst possible rating (e.g., 1)",
        verbose_name="Минимальный рейтинг"
    )

    def __str__(self):
        return f"Rating for {self.page}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class CalculatorOption(models.Model):
    """
    Stores options for the calculator (vehicle types, categories, etc.).
    """
    OPTION_TYPES = [
        ('vehicle_type', 'Тип транспортного средства'),
        ('category', 'Категория'),
        ('extra', 'Дополнительный параметр')
    ]
    option_type = models.CharField(
        max_length=50, 
        choices=OPTION_TYPES, 
        help_text="Type of option",
        verbose_name="Тип опции"
    )
    name = models.CharField(
        max_length=255, 
        help_text="Option name (e.g., 'Седан')",
        verbose_name="Название опции"
    )
    value = models.CharField(
        max_length=50, 
        help_text="Option value (e.g., '1')",
        verbose_name="Значение"
    )
    discount = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Discount value (e.g., '5')",
        verbose_name="Скидка"
    )
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        help_text="Parent option for hierarchical options",
        verbose_name="Родительская опция"
    )

    def __str__(self):
        return f"{self.option_type}: {self.name}"

    class Meta:
        verbose_name = "Опция калькулятора"
        verbose_name_plural = "Опции калькулятора"