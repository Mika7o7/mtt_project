# core/admin.py
from django.contrib import admin
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto,
    FAQ, Rating, Article, District, MetroStation,
    City
)

# ==== КАСТОМНЫЙ АДМИН-САЙТ (ТВОЙ КРАСИВЫЙ ДИЗАЙН) ====
class CustomAdminSite(admin.AdminSite):
    site_header = "Главная страница"
    site_title = "Админка MTT Project"
    index_title = "Управление контентом"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        main_model_order = [
            "HeroSection", "HowToOrderStep", "TransportType",
            "WhyChooseUs", "InfoSection", "PriceItem", "WorkPhoto",
            "FAQ", "Rating", "District", "MetroStation", "City"
        ]
        article_model_order = ["Article"]

        main_models = []
        for app in app_list:
            for model in app.get('models', []):
                if model['object_name'] in main_model_order:
                    main_models.append(model)

        article_models = []
        for app in app_list:
            for model in app.get('models', []):
                if model['object_name'] in article_model_order:
                    article_models.append(model)

        new_app_list = [
            {"name": "Главная страница", "app_label": "core", "models": main_models},
            {"name": "Наши услуги", "app_label": "core", "models": []},
            {"name": "О нас", "app_label": "core", "models": []},
            {"name": "Статья", "app_label": "core", "models": article_models},
            {"name": "Цены", "app_label": "core", "models": []},
            {"name": "Галерея", "app_label": "core", "models": []},
            {"name": "Калькулятор", "app_label": "core", "models": []},
            {"name": "Оплата", "app_label": "core", "models": []},
        ]
        return new_app_list


custom_admin_site = CustomAdminSite(name='custom_admin')


# ===== TransportType — САМАЯ КРУТАЯ АДМИНКА =====
@admin.register(TransportType, site=custom_admin_site)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "price_from", "button_text")
    list_editable = ("price_from", "button_text")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("gallery",)
    list_per_page = 20

    fieldsets = (
        ("Основное", {
            "fields": ("name", "slug", "image", "icon", "button_text", "price_from")
        }),
        ("Контент детальной страницы", {
            "fields": ("description", "features", "gallery")
        }),
    )


# ===== Остальные модели — ВСЁ ИСПРАВЛЕНО =====
@admin.register(HeroSection, site=custom_admin_site)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")

@admin.register(HowToOrderStep, site=custom_admin_site)
class HowToOrderStepAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "get_icon")
    list_editable = ("order",)                     # order можно редактировать
    list_display_links = ("title",)                # кликаем по названию
    ordering = ("order",)

    def get_icon(self, obj):
        return "Icon" if obj.icon else "—"
    get_icon.short_description = "Иконка"

@admin.register(WhyChooseUs, site=custom_admin_site)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(InfoSection, site=custom_admin_site)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text")

@admin.register(PriceItem, site=custom_admin_site)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    list_editable = ("price",)
    search_fields = ("title",)

@admin.register(WorkPhoto, site=custom_admin_site)
class WorkPhotoAdmin(admin.ModelAdmin):
    list_display = ("caption_or_filename",)
    search_fields = ("caption",)

    def caption_or_filename(self, obj):
        return obj.caption or obj.image.name.split("/")[-1][:40]
    caption_or_filename.short_description = "Фото"

@admin.register(FAQ, site=custom_admin_site)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active")
    list_editable = ("is_active",)
    search_fields = ("question", "answer")

@admin.register(Rating, site=custom_admin_site)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("page", "stars", "votes")

@admin.register(Article, site=custom_admin_site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title", "text")
    ordering = ("-date",)

@admin.register(District, site=custom_admin_site)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("short_name", "name", "metro_count")
    search_fields = ("name", "short_name")
    prepopulated_fields = {"slug": ("short_name",)}
    list_editable = ("metro_count",)

@admin.register(MetroStation, site=custom_admin_site)
class MetroStationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(City, site=custom_admin_site)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}