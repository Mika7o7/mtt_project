# core/admin.py
from django.contrib import admin
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto, FAQ, Rating, Article
)

# ==== Кастомный админ-сайт ====
class CustomAdminSite(admin.AdminSite):
    site_header = "Главная страница"
    site_title = "Админка MTT Project"
    index_title = "Управление контентом"

    def get_app_list(self, request):
        """
        Переопределяем порядок показа моделей и групп
        """
        app_list = super().get_app_list(request)

        # ==== Определяем порядок моделей ====
        model_order = [
            "HeroSection",
            "HowToOrderStep",
            "TransportType",
            "WhyChooseUs",
            "InfoSection",
            "PriceItem",
            "WorkPhoto",
            "FAQ",
            "Rating"
        ]

        article_order = [
            "Article",
        ]

        # ==== Главная страница ====
        main_models = []
        for app in app_list:
            for model_name in model_order:
                for model in app['models']:
                    if model['object_name'] == model_name:
                        main_models.append(model)

        # ==== Статья страница ====
        article_models = []
        for app in app_list:
            for model_name in article_order:
                for model in app['models']:
                    if model['object_name'] == model_name:
                        article_models.append(model)

        # ==== Создаём все группы ====
        new_app_list = [
            {
                "name": "Главная страница",
                "app_label": "core",
                "models": main_models
            },
            {
                "name": "Наши услуги",
                "app_label": "core",
                "models": [
                    # TODO: добавить модели для раздела "Наши услуги"
                ]
            },
            {
                "name": "О нас",
                "app_label": "core",
                "models": [
                    # TODO: добавить модели для раздела "О нас"
                ]
            },
            {
                "name": "Статья",
                "app_label": "core",
                "models": article_models
            },
            {
                "name": "Цены",
                "app_label": "core",
                "models": [
                    # TODO: добавить модели для раздела "Цены"
                ]
            },
            {
                "name": "Галерея",
                "app_label": "core",
                "models": [
                    # TODO: добавить модели для раздела "Галерея"
                ]
            },
            {
                "name": "Калькулятор",
                "app_label": "core",
                "models": [
                    # TODO: добавить модели для раздела "Калькулятор"
                ]
            },
            {
                "name": "Оплата",
                "app_label": "core",
                "models": [
                    # TODO: добавить модели для раздела "Оплата"
                ]
            },
        ]

        return new_app_list

# ==== Регистрируем кастомный админ-сайт ====
custom_admin_site = CustomAdminSite(name='custom_admin')

# ===== Регистрация моделей ====
@admin.register(HeroSection, site=custom_admin_site)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")


@admin.register(HowToOrderStep, site=custom_admin_site)
class HowToOrderStepAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "icon")


@admin.register(TransportType, site=custom_admin_site)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "button_text")


@admin.register(WhyChooseUs, site=custom_admin_site)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("title", "icon")


@admin.register(InfoSection, site=custom_admin_site)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text")


@admin.register(PriceItem, site=custom_admin_site)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price")


@admin.register(WorkPhoto, site=custom_admin_site)
class WorkPhotoAdmin(admin.ModelAdmin):
    list_display = ("caption", "image")


@admin.register(FAQ, site=custom_admin_site)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active")


@admin.register(Rating, site=custom_admin_site)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("page", "stars", "votes")

@admin.register(Article, site=custom_admin_site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "date")

