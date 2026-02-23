# core/admin.py
from django.contrib import admin
from django import forms
from .models import (
    HeroSection, HowToOrderStep, TransportType,
    WhyChooseUs, InfoSection, PriceItem, WorkPhoto,
    FAQ, Article, Page
)

# ==== КАСТОМНЫЙ АДМИН-САЙТ ====
class CustomAdminSite(admin.AdminSite):
    site_header = "Модули"
    site_title = "Админка MTT Project"
    index_title = "Управление контентом"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        main_model_order = [
            "HeroSection", "HowToOrderStep", "TransportType",
            "WhyChooseUs", "InfoSection", "PriceItem", "WorkPhoto",
            "FAQ", "Article",
        ]
        
        pages = [
            "Page"
        ]

        main_models = []
        pages_models = []
        for app in app_list:
            for model in app.get('models', []):
                if model['object_name'] in main_model_order:
                    main_models.append(model)
                elif model['object_name'] in pages:
                    pages_models.append(model)
               
        new_app_list = [
            {"name": "Модули", "app_label": "core", "models": main_models},
            {"name": "Страницы", "app_label": "core", "models": pages_models},
        ]
        return new_app_list


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
    
    # Используем только fieldsets
    fieldsets = (
        (None, {
            "fields": ("title", "text")
        }),
        ("Дата создания", {
            "fields": ("date",),
            "classes": ("collapse",),  # сворачиваемый блок
        }),
    )
    
    # Показываем date как read-only
    readonly_fields = ('date',)


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'hero_sections': forms.CheckboxSelectMultiple,
            'how_to_order_steps': forms.CheckboxSelectMultiple,
            'transport_types': forms.CheckboxSelectMultiple,
            'why_choose_us': forms.CheckboxSelectMultiple,
            'info_sections': forms.CheckboxSelectMultiple,
            'price_items': forms.CheckboxSelectMultiple,
            'work_photos': forms.CheckboxSelectMultiple,
            'faqs': forms.CheckboxSelectMultiple,
            'articles': forms.CheckboxSelectMultiple,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Проверяем, существует ли поле slug в форме
        if 'slug' in self.fields:
            # Для главной страницы
            if self.instance and self.instance.pk and self.instance.is_homepage:
                self.fields['slug'].required = False
                self.fields['slug'].help_text = "Главная страница не должна иметь slug"
                self.fields['slug'].widget.attrs['readonly'] = True
            else:
                # Для обычных страниц
                self.fields['slug'].required = True
                self.fields['slug'].help_text = "URL страницы. Можно использовать слеши (/), латиницу, цифры и дефисы. Например: oblasti/evakuator/evakuator-aleshino"
                self.fields['slug'].widget.attrs['placeholder'] = 'oblasti/evakuator/evakuator-aleshino'
    
    def clean_slug(self):
        """Валидация slug"""
        # Проверяем, есть ли поле slug в cleaned_data
        if 'slug' not in self.cleaned_data:
            return None
            
        slug = self.cleaned_data.get('slug')
        is_homepage = self.cleaned_data.get('is_homepage')
        
        # Если это главная страница, slug должен быть пустым
        if is_homepage:
            return ''
        
        # Для неглавных страниц slug обязателен
        if not slug:
            raise forms.ValidationError("Обычные страницы должны иметь slug")
        
        # Проверяем формат slug (буквы, цифры, дефисы, слеши)
        import re
        # Разрешаем: латиница, цифры, дефисы, слеши
        if not re.match(r'^[a-z0-9-/]+$', slug.lower()):
            raise forms.ValidationError(
                "Slug может содержать только латинские буквы в нижнем регистре, "
                "цифры, дефисы и слеши (/)"
            )
        
        # Проверяем, что нет двойных слешей
        if '//' in slug:
            raise forms.ValidationError("Slug не может содержать двойные слеши")
        
        # Проверяем, что слеши не в начале и не в конце
        if slug.startswith('/') or slug.endswith('/'):
            raise forms.ValidationError("Slug не может начинаться или заканчиваться слешем")
        
        # Проверяем уникальность
        if Page.objects.filter(slug=slug).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Страница с таким slug уже существует")
        
        return slug
    
    def clean(self):
        cleaned_data = super().clean()
        is_homepage = cleaned_data.get('is_homepage')
        
        # Проверяем наличие slug в cleaned_data только если это не главная страница
        if not is_homepage and 'slug' in cleaned_data:
            slug = cleaned_data.get('slug')
            if not slug:
                self.add_error('slug', "Обычные страницы должны иметь slug")
        
        # Проверка для главной страницы
        if is_homepage and 'slug' in cleaned_data:
            slug = cleaned_data.get('slug')
            if slug:
                self.add_error('slug', "Главная страница не должна иметь slug")
        
        return cleaned_data


@admin.register(Page, site=custom_admin_site)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    filter_horizontal = (
        'hero_sections', 'how_to_order_steps', 'transport_types',
        'why_choose_us', 'info_sections', 'price_items', 'work_photos',
        'faqs', 'articles',
    )
    
    list_display = ('name', 'page_type', 'is_homepage', 'is_active', 'order', 'slug_preview')
    list_editable = ('order', 'is_active')
    list_filter = ('page_type', 'is_homepage', 'is_active')
    list_per_page = 20
    
    search_fields = ('name', 'slug', 'info_name', 'page_title', 'meta_title')
    
    date_hierarchy = 'created_at'
    
    def slug_preview(self, obj):
        """Предпросмотр URL"""
        if obj.is_homepage:
            return '/'
        if obj.slug:
            return f'/{obj.slug}/'
        return '-'
    slug_preview.short_description = 'URL'
    
    def get_fieldsets(self, request, obj=None):
        # Для главной страницы - исключаем slug из полей
        if obj and obj.is_homepage:
            base_fields = ('page_type', 'name', 'is_homepage', 'is_active', 'order')
        else:
            base_fields = ('page_type', 'name', 'slug', 'is_homepage', 'is_active', 'order')
        
        fieldsets = [
            ('Основная информация', {
                'fields': base_fields
            }),
            ('SEO информация', {
                'fields': ('info_name', 'sub_description', 'page_title', 'page_text',
                          'meta_title', 'meta_description', 'meta_keywords')
            }),
            ('Настройки отображения', {
                'fields': ('fastorder', 'calculator', 'question_map', 
                          'map_show', 'payment_show', 'second_hero_section')
            }),
            ('Контент страницы', {
                'fields': (
                    'hero_sections',
                    'how_to_order_steps',
                    'transport_types',
                    'why_choose_us',
                    'info_sections',
                    'price_items',
                    'work_photos',
                    'faqs',
                    'articles',
                ),
            }),
        ]
        
        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        """Поля только для чтения"""
        readonly = []
        if obj and obj.is_homepage:
            # Для главной страницы slug должен быть только для чтения
            readonly.append('slug')
        return readonly