# core/admin.py
from django.contrib import admin
from django import forms
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto,
    FAQ, Rating, Article, District, MetroStation,
    City, Gruzovoy, Manipulyator, Highway, Region,
    AboutPage, ArticlePage, PricePage, GalleryPage,
    CalculatorPage, Page
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
            "FAQ", "Rating", "Article",
            
        ]
        evacuation = [
            "District", "MetroStation", "City",
            "Gruzovoy", "Manipulyator", "Highway", "Region",
        ]
        pages = [
            "AboutPage", "ArticlePage", "PricePage", "GalleryPage",
            "CalculatorPage", "Page"
        ]


        main_models = []
        pages_models = []
        evacuation_models = []
        for app in app_list:
            for model in app.get('models', []):
                if model['object_name'] in main_model_order:
                    main_models.append(model)
                elif model['object_name'] in pages:
                    pages_models.append(model)
                elif model['object_name'] in evacuation:
                    evacuation_models.append(model)
                    
       
        new_app_list = [
            {"name": "Главная страница", "app_label": "core", "models": main_models},
            {"name": "страницы", "app_label": "core", "models": pages_models},
            {"name": "Эвакуация по", "app_label": "core", "models": evacuation_models},
          
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
    list_display = ("short_name", "name")
    search_fields = ("name", "short_name")
    prepopulated_fields = {"slug": ("short_name",)}

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


@admin.register(Gruzovoy, site=custom_admin_site)
class GruzovoyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "info_name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Manipulyator, site=custom_admin_site)
class ManipulyatorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "info_name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Highway, site=custom_admin_site)
class HighwayAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "info_name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Region, site=custom_admin_site)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(AboutPage, site=custom_admin_site)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("info_name",)
    search_fields = ("info_name",)


@admin.register(ArticlePage, site=custom_admin_site)
class ArticlePageAdmin(admin.ModelAdmin):
    list_display = ("info_name",)
    search_fields = ("info_name",)


@admin.register(PricePage, site=custom_admin_site)
class PricePageAdmin(admin.ModelAdmin):
    list_display = ("info_name",)
    search_fields = ("info_name",)


@admin.register(GalleryPage, site=custom_admin_site)
class GalleryPageAdmin(admin.ModelAdmin):
    list_display = ("info_name",)
    search_fields = ("info_name",)


@admin.register(CalculatorPage, site=custom_admin_site)
class CalculatorPageAdmin(admin.ModelAdmin):
    list_display = ("info_name",)
    search_fields = ("info_name",)


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        is_homepage = cleaned_data.get('is_homepage')
        slug = cleaned_data.get('slug')
        
        if is_homepage and slug:
            raise forms.ValidationError("Главная страница не должна иметь slug")
        
        if not is_homepage and not slug:
            raise forms.ValidationError("Обычные страницы должны иметь slug")
        
        return cleaned_data


@admin.register(Page, site=custom_admin_site)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    # Настраиваем отображение полей в зависимости от типа страницы
    def get_fieldsets(self, request, obj=None):
        if obj and obj.is_homepage:
            # Для главной страницы не показываем поле slug
            return (
                ('Основная информация', {
                    'fields': ('name', 'is_homepage', 'is_active', 'order')
                }),
                ('SEO информация', {
                    'fields': ('info_name', 'sub_description', 'page_title', 'page_text',
                              'meta_title', 'meta_description', 'meta_keywords')
                }),
                ('Контент страницы', {
                    'fields': (
                        'hero_sections',
                        'how_to_order_steps',
                        'transport_types',
                        'why_choose_us',
                        'fastorder',
                        'calculator',
                        'question_map',
                        'map_show',
                        'payment_show',
                        'second_hero_section',
                        'info_sections',
                        'price_items',
                        'work_photos',
                        'faqs',
                        'ratings',
                        'articles',
                        'cities',
                        'metro_stations',
                        'regions',
                        'districts',
                        'gruzovoys',
                        'manipulyators',
                        'highways',
                    ),
                }),
            )
        else:
            # Для обычных страниц показываем все поля
            return (
                ('Основная информация', {
                    'fields': ('name', 'slug', 'is_homepage', 'is_active', 'order')
                }),
                ('SEO информация', {
                    'fields': ('info_name', 'sub_description', 'page_title', 'page_text',
                              'meta_title', 'meta_description', 'meta_keywords')
                }),
                ('Контент страницы', {
                    'fields': (
                        'hero_sections',
                        'how_to_order_steps',
                        'transport_types',
                        'why_choose_us',
                        'fastorder',
                        'calculator',
                        'question_map',
                        'map_show',
                        'payment_show',
                        'second_hero_section',
                        'info_sections',
                        'price_items',
                        'work_photos',
                        'faqs',
                        'ratings',
                        'articles',
                        'cities',
                        'metro_stations',
                        'regions',
                        'districts',
                        'gruzovoys',
                        'manipulyators',
                        'highways',
                    ),
                }),
            )