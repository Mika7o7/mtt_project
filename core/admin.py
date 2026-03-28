from django.contrib import admin
from django.db.models import Q
from django.db.models.functions import Lower, Upper
from django import forms
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto,
    FAQ, Article, Page, CalculatorVehicleType, CalculatorCategory, CalculatorExtraService
)


class CustomAdminSite(admin.AdminSite):
    site_header = "Модули"
    site_title = "Админка MTT Project"
    index_title = "Управление контентом"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Модели для раздела "Модули"
        main_model_order = [
            "HeroSection", "HowToOrderStep", "TransportType",
            "WhyChooseUs", "InfoSection", "PriceItem", "WorkPhoto",
            "FAQ", "Article",
        ]
        
        # Модели для раздела "Страницы"
        pages = ["Page"]
        
        # Модели для раздела "Калькулятор"
        calculator_models = [
            "CalculatorVehicleType", "CalculatorCategory", "CalculatorExtraService"
        ]

        main_models = []
        pages_models = []
        calculator_models_list = []

        for app in app_list:
            for model in app.get('models', []):
                if model['object_name'] in main_model_order:
                    main_models.append(model)
                elif model['object_name'] in pages:
                    pages_models.append(model)
                elif model['object_name'] in calculator_models:
                    calculator_models_list.append(model)

        return [
            {"name": "Модули", "app_label": "core", "models": main_models},
            {"name": "Калькулятор", "app_label": "core", "models": calculator_models_list},
            {"name": "Страницы", "app_label": "core", "models": pages_models},
        ]


custom_admin_site = CustomAdminSite(name='custom_admin')


# ===== TransportType =====
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


# ===== HeroSection =====
@admin.register(HeroSection, site=custom_admin_site)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    search_fields = ("title", "subtitle")

    fieldsets = (
        (None, {
            "fields": ("title", "subtitle", "button_text", "model_3d")
        }),
    )


# ===== HowToOrderStep =====
@admin.register(HowToOrderStep, site=custom_admin_site)
class HowToOrderStepAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "get_icon")
    list_editable = ("order",)
    list_display_links = ("title",)
    search_fields = ("title", "description")
    ordering = ("order",)

    def get_icon(self, obj):
        return obj.icon or "—"
    get_icon.short_description = "Иконка"

    fieldsets = (
        (None, {
            "fields": ("order", "icon", "title", "description", "image")
        }),
    )


# ===== WhyChooseUs =====
@admin.register(WhyChooseUs, site=custom_admin_site)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title", "description")

    fieldsets = (
        (None, {
            "fields": ("icon", "title", "description")
        }),
    )


# ===== InfoSection =====
@admin.register(InfoSection, site=custom_admin_site)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text")
    search_fields = ("title", "text", "button_text")

    fieldsets = (
        (None, {
            "fields": ("image", "title", "text", "button_text")
        }),
    )


# ===== PriceItem =====
@admin.register(PriceItem, site=custom_admin_site)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    list_editable = ("price",)
    search_fields = ("title",)

    fieldsets = (
        (None, {
            "fields": ("title", "price")
        }),
    )


# ===== WorkPhoto =====
@admin.register(WorkPhoto, site=custom_admin_site)
class WorkPhotoAdmin(admin.ModelAdmin):
    list_display = ("caption_or_filename",)
    search_fields = ("caption",)

    def caption_or_filename(self, obj):
        return obj.caption or f"Фото {obj.id}"
    caption_or_filename.short_description = "Фото"

    fieldsets = (
        (None, {
            "fields": ("image", "caption")
        }),
    )


# ===== FAQ =====
@admin.register(FAQ, site=custom_admin_site)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("question", "answer")

    fieldsets = (
        (None, {
            "fields": ("question", "answer", "is_active")
        }),
    )


# ===== Article =====
@admin.register(Article, site=custom_admin_site)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title", "text")
    date_hierarchy = "date"
    ordering = ("-date",)
    readonly_fields = ("date",)

    fieldsets = (
        (None, {
            "fields": ("title", "text")
        }),
        ("Дата создания", {
            "fields": ("date",),
            "classes": ("collapse",),
        }),
    )


# ===== Page Form =====
class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        is_homepage = self.cleaned_data.get("is_homepage")

        if is_homepage:
            return ""

        if not slug:
            raise forms.ValidationError("Обычные страницы должны иметь slug")

        import re
        if not re.match(r"^[a-z0-9-/]+$", slug.lower()):
            raise forms.ValidationError(
                "Slug может содержать только латинские буквы в нижнем регистре, "
                "цифры, дефисы и слеши (/)"
            )

        if "//" in slug:
            raise forms.ValidationError("Slug не может содержать двойные слеши")

        if slug.startswith("/") or slug.endswith("/"):
            raise forms.ValidationError(
                "Slug не может начинаться или заканчиваться слешем"
            )

        if Page.objects.filter(slug__iexact=slug).exclude(
            id=self.instance.id
        ).exists():
            raise forms.ValidationError(
                "Страница с таким slug уже существует"
            )

        return slug





# ===== Page Admin =====
@admin.register(Page, site=custom_admin_site)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm

    list_display = (
        "name",
        "page_type",
        "is_homepage",
        "is_active",
        "order",
        "slug_preview",
    )
    list_editable = ("order", "is_active")
    list_filter = ("page_type", "is_homepage", "is_active")
    list_per_page = 20

    # ВАЖНО: search_fields должен быть, чтобы поле поиска отображалось
    search_fields = ('name',)  # ← добавил, чтобы поле поиска было видно

    date_hierarchy = "created_at"

    filter_horizontal = (
        "hero_sections",
        "how_to_order_steps",
        "transport_types",
        "why_choose_us",
        "info_sections",
        "price_items",
        "work_photos",
        "faqs",
        "articles",
    )

    def get_search_results(self, request, queryset, search_term):
        """
        Поиск с нормализацией регистра для SQLite
        """
        if search_term:
            # Приводим поисковый запрос к верхнему регистру
            term_upper = search_term.upper()
            
            # Используем аннотацию для нормализации
            queryset = queryset.annotate(
                name_upper=Upper('name')
            ).filter(
                Q(name_upper__contains=term_upper) |
                Q(slug__icontains=search_term) |
                Q(info_name__icontains=search_term) |
                Q(page_title__icontains=search_term) |
                Q(meta_title__icontains=search_term) |
                Q(sub_description__icontains=search_term) |
                Q(page_text__icontains=search_term)
            ).distinct()
        
        return queryset, False

    def slug_preview(self, obj):
        if obj.is_homepage:
            return "/"
        if obj.slug:
            return f"/{obj.slug}/"
        return "-"
    slug_preview.short_description = "URL"

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_homepage:
            return ("slug",)
        return ()
    

@admin.register(CalculatorVehicleType, site=custom_admin_site)
class CalculatorVehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'order')
    list_editable = ('order',)
    list_filter = ('vehicle_type',)
    search_fields = ('name',)


@admin.register(CalculatorCategory, site=custom_admin_site)
class CalculatorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'price_per_100km', 'order')
    list_editable = ('price_per_100km', 'order')
    list_filter = ('vehicle_type',)
    search_fields = ('name',)
    autocomplete_fields = ('vehicle_type',)


@admin.register(CalculatorExtraService, site=custom_admin_site)
class CalculatorExtraServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'vehicle_type', 'order')
    list_editable = ('price', 'order')
    list_filter = ('vehicle_type',)
    search_fields = ('name',)