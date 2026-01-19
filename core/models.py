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


# ===== TRANSPORT TYPES =====
# class TransportType(models.Model):
#     name = models.CharField("Название типа", max_length=100)
#     image = models.ImageField("Фото транспорта", upload_to="transport/")
#     button_text = models.CharField("Текст кнопки", max_length=50, default="Заказать")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Тип транспорта"
#         verbose_name_plural = "Типы транспорта"

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

# ===== RATING =====
class Rating(models.Model):
    page = models.CharField("Страница", max_length=100, unique=True)
    stars = models.FloatField("Оценка", default=0)
    votes = models.PositiveIntegerField("Количество голосов", default=0)

    def __str__(self):
        return f"{self.page}: {self.stars} ⭐ ({self.votes} голосов)"

    class Meta:
        verbose_name = "Рейтинг страницы"
        verbose_name_plural = "Рейтинги страниц"


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
    

# ===== ГОРОДА МО (новая модель) =====
class City(models.Model):
    name = models.CharField("Название города", max_length=100)  # например: Химки
    slug = models.SlugField(
        "ЧПУ (khimki)",
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    
    # Новые поля — как ты хотел
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
                                help_text="Например: Эвакуатор в Химках — недорого и быстро")
    
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Город МО"
        verbose_name_plural = "Города МО"
        ordering = ['name']

    def __str__(self):
        return self.name


# ===== МЕТРО — обновлено =====
class MetroStation(models.Model):
    name = models.CharField("Название станции", max_length=100)
    slug = models.SlugField(
        "ЧПУ (salarevo)",
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    # ← НОВЫЕ ПОЛЯ!
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
                                help_text="Например: Эвакуатор у метро Саларьево — от 2500 ₽")

    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Станция метро"
        verbose_name_plural = "Станции метро"
        ordering = ['name']

    def __str__(self):
        return self.name

# ===== Область — обновлено =====
class Region(models.Model):
    name = models.CharField("Название станции", max_length=100)
    slug = models.SlugField(
        "ЧПУ (salarevo)",
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    # ← НОВЫЕ ПОЛЯ!
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
                                help_text="Например: Эвакуатор у метро Саларьево — от 2500 ₽")

    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Станция область"
        verbose_name_plural = "Станции область"
        ordering = ['name']

    def __str__(self):
        return self.name
    

# ===== ОКРУГА — обновлено =====
class District(models.Model):
    name = models.CharField("Название округа", max_length=100)
    slug = models.SlugField(
        "ЧПУ (vao)",
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    short_name = models.CharField("Короткое название", max_length=20)

    # ← НОВЫЕ ПОЛЯ!
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
                                help_text="Например: Эвакуатор в ВАО — Восточный округ Москвы")
    image = models.ImageField("Фото округа", upload_to="districts/", blank=True, null=True)
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Округ Москвы"
        verbose_name_plural = "Округа Москвы"
        ordering = ['name']

    def __str__(self):
        return self.name


# 1. Грузовые эвакуаторы — отдельная модель
class Gruzovoy(models.Model):
    name = models.CharField("Название (например: Грузовой эвакуатор до 10 тонн)", max_length=150)
    slug = models.SlugField("ЧПУ (gruzovoy-evakuator-do-10-tonn)", max_length=150, unique=True)
    
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
        help_text="Например: Грузовой эвакуатор в Москве и области — от 8000 ₽")
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Грузовой эвакуатор"
        verbose_name_plural = "Грузовые эвакуаторы"
        ordering = ['name']

    def __str__(self):
        return self.name


# 2. Манипуляторы — отдельная модель
class Manipulyator(models.Model):
    name = models.CharField("Название (например: Эвакуатор с манипулятором)", max_length=150)
    slug = models.SlugField("ЧПУ (manipulyator)", max_length=150, unique=True)
    
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
        help_text="Например: Эвакуатор с краном-манипулятором в Москве")
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Эвакуатор-манипулятор"
        verbose_name_plural = "Эвакуаторы-манипуляторы"
        ordering = ['name']

    def __str__(self):
        return self.name


# 3. Шоссе — отдельная модель
class Highway(models.Model):
    name = models.CharField("Название шоссе", max_length=100)  # Дмитровское шоссе
    slug = models.SlugField("ЧПУ (dmitrovskoe-shosse)", max_length=120, unique=True)
    
    info_name = models.CharField("Заголовок страницы (H1)", max_length=150, blank=True,
        help_text="Например: Эвакуатор по Дмитровскому шоссе — быстро и недорого")
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)

    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField("SEO-описание для детальной страницы", blank=True)
    meta_keywords = models.TextField("SEO-Ключевые слова для детальной страницы", blank=True,
        help_text="Например: эвакуатор услуги, эвакуация авто москва, грузовой эвакуатор")

    class Meta:
        verbose_name = "Шоссе"
        verbose_name_plural = "Шоссе"
        ordering = ['name']

    def __str__(self):
        return self.name


class AboutPage(models.Model):
    info_name = models.CharField(
        "Заголовок страницы (H1)", 
        max_length=150, 
        blank=True,
        help_text="Например: О нашей компании — профессиональные услуги эвакуации"
    )
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)
    
    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField(
        "SEO-описание для детальной страницы", 
        blank=True
    )
    meta_keywords = models.TextField(
        "SEO-Ключевые слова для детальной страницы", 
        blank=True,
        help_text="Например: о компании эвакуатор, история компании, наши преимущества"
    )
    
    class Meta:
        verbose_name = "Страница 'О нас'"
        verbose_name_plural = "Страница 'О нас'"
    
    def __str__(self):
        return self.info_name if self.info_name else "Страница 'О нас'"
    

class ArticlePage(models.Model):
    info_name = models.CharField(
        "Заголовок страницы (H1)", 
        max_length=150, 
        blank=True,
        help_text="Например: Полезные статьи об услугах эвакуации"
    )
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)
    
    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField(
        "SEO-описание для детальной страницы", 
        blank=True
    )
    meta_keywords = models.TextField(
        "SEO-Ключевые слова для детальной страницы", 
        blank=True,
        help_text="Например: статьи про эвакуацию, советы автомобилистам, полезная информация"
    )
    
    class Meta:
        verbose_name = "Страница 'Статьи'"
        verbose_name_plural = "Страница 'Статьи'"
    
    def __str__(self):
        return self.info_name if self.info_name else "Страница 'Статьи'"
    

class PricePage(models.Model):
    info_name = models.CharField(
        "Заголовок страницы (H1)", 
        max_length=150, 
        blank=True,
        help_text="Например: Цены на услуги эвакуатора в Москве и области"
    )
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)
    
    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField(
        "SEO-описание для детальной страницы", 
        blank=True
    )
    meta_keywords = models.TextField(
        "SEO-Ключевые слова для детальной страницы", 
        blank=True,
        help_text="Например: цены на эвакуатор, стоимость услуг, прайс-лист эвакуация"
    )
    
    class Meta:
        verbose_name = "Страница 'Цены'"
        verbose_name_plural = "Страница 'Цены'"
    
    def __str__(self):
        return self.info_name if self.info_name else "Страница 'Цены'"
    

class GalleryPage(models.Model):
    info_name = models.CharField(
        "Заголовок страницы (H1)", 
        max_length=150, 
        blank=True,
        help_text="Например: Фотогалерея наших работ и эвакуаторов"
    )
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)
    
    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField(
        "SEO-описание для детальной страницы", 
        blank=True
    )
    meta_keywords = models.TextField(
        "SEO-Ключевые слова для детальной страницы", 
        blank=True,
        help_text="Например: фото эвакуаторов, галерея работ, наши автомобили"
    )
    
    class Meta:
        verbose_name = "Страница 'Галерея'"
        verbose_name_plural = "Страница 'Галерея'"
    
    def __str__(self):
        return self.info_name if self.info_name else "Страница 'Галерея'"
    

class CalculatorPage(models.Model):
    info_name = models.CharField(
        "Заголовок страницы (H1)", 
        max_length=150, 
        blank=True,
        help_text="Например: Расчет стоимости эвакуации автомобиля"
    )
    sub_description = models.TextField("Под заголовок", blank=True)
    page_title = models.CharField("Заголовок текста", max_length=150, blank=True)
    page_text = models.TextField("Текст страницы", blank=True)
    
    meta_title = models.CharField("SEO-Заголовок", max_length=150, blank=True)
    meta_description = models.TextField(
        "SEO-описание для детальной страницы", 
        blank=True
    )
    meta_keywords = models.TextField(
        "SEO-Ключевые слова для детальной страницы", 
        blank=True,
        help_text="Например: калькулятор эвакуации, рассчитать стоимость, онлайн расчет"
    )
    
    class Meta:
        verbose_name = "Страница 'Калькулятор'"
        verbose_name_plural = "Страница 'Калькулятор'"
    
    def __str__(self):
        return self.info_name if self.info_name else "Страница 'Калькулятор'"
