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
class TransportType(models.Model):
    name = models.CharField("Название типа", max_length=100)
    image = models.ImageField("Фото транспорта", upload_to="transport/")
    button_text = models.CharField("Текст кнопки", max_length=50, default="Заказать")

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