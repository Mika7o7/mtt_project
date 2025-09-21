from django.db import models
from django.utils.text import slugify

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, max_length=200, verbose_name='URL-имя')
    content = models.TextField(verbose_name='Контент (HTML)')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название услуги')
    slug = models.SlugField(unique=True, max_length=100, verbose_name='URL-имя')
    description = models.TextField(verbose_name='Описание')
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена за км')
    image = models.ImageField(upload_to='services/', blank=True, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название документа')
    file = models.FileField(upload_to='documents/', verbose_name='Файл (PDF)')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

class Review(models.Model):
    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(default=5, verbose_name='Рейтинг')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f'{self.author} - {self.rating}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'