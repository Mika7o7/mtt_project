from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import (
    MetaData, HeroSection, District, OrderStep, FormConfig, VideoReview,
    Photo, Price, Service, WhyChooseUs, FAQ, Rating, CalculatorOption
)

class CustomAdminSite(AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        ordered_models = [
            'MetaData',
            'HeroSection',
            'District',
            'OrderStep',
            'FormConfig',
            'VideoReview',
            'Photo',
            'Price',
            'Service',
            'WhyChooseUs',
            'FAQ',
            'Rating',
            'CalculatorOption',
        ]
        for app in app_list:
            if app['app_label'] == 'core':
                app['models'].sort(key=lambda x: ordered_models.index(x['object_name']))
        return app_list

# Создаём экземпляр кастомного AdminSite
custom_admin_site = CustomAdminSite(name='custom_admin')


# Определяем классы ModelAdmin
class MetaDataAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'canonical_url_name']
    search_fields = ['page', 'title', 'keywords', 'description']
    list_filter = ['page']
    ordering = ['page']
    fieldsets = (
        (None, {
            'fields': ('page', 'title', 'keywords', 'description')
        }),
        ('Open Graph', {
            'fields': ('og_url', 'og_title', 'og_image', 'og_description')
        }),
        ('Canonical URL', {
            'fields': ('canonical_url_name',)
        }),
    )

class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'low_price', 'price_currency']
    search_fields = ['page', 'title', 'description']
    list_filter = ['page', 'price_currency']
    ordering = ['page']
    fieldsets = (
        (None, {
            'fields': ('page', 'title', 'description', 'background_image')
        }),
        ('Offer Details', {
            'fields': ('low_price', 'price_currency', 'availability_url', 'url_name')
        }),
    )

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'url_name']
    search_fields = ['name', 'slug', 'url_name']
    list_filter = ['url_name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}

class OrderStepAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'description_preview']
    search_fields = ['title', 'description']
    list_filter = ['order']
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon', 'number_icon', 'order')
        }),
    )

    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Описание (превью)'

class FormConfigAdmin(admin.ModelAdmin):
    list_display = ['form_id', 'title', 'f_vid', 'page_id', 'dop_id']
    search_fields = ['form_id', 'title', 'f_vid', 'page_id', 'dop_id']
    list_filter = ['form_id']
    ordering = ['form_id']
    fieldsets = (
        (None, {
            'fields': ('form_id', 'title', 'background_image')
        }),
        ('Hidden Fields', {
            'fields': ('f_vid', 'page_id', 'dop_id')
        }),
    )

class VideoReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_url', 'order']
    search_fields = ['title', 'youtube_url']
    list_filter = ['order']
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': ('title', 'youtube_url', 'thumbnail', 'order')
        }),
    )

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'order', 'image_preview']
    search_fields = ['caption']
    list_filter = ['order']
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': ('image', 'thumbnail', 'caption', 'order')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return '<img src="%s" style="max-height: 50px;" />' % obj.image.url
        return 'Нет изображения'
    image_preview.allow_tags = True
    image_preview.short_description = 'Превью изображения'

class PriceAdmin(admin.ModelAdmin):
    list_display = ['service', 'price']
    search_fields = ['service', 'price']
    ordering = ['service']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_name', 'description_preview']
    search_fields = ['title', 'description', 'url_name']
    list_filter = ['url_name']
    ordering = ['title']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'url_name')
        }),
    )

    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Описание (превью)'

class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'description_preview']
    search_fields = ['title', 'description']
    list_filter = ['order']
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon', 'order')
        }),
    )

    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Описание (превью)'

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'answer_preview']
    search_fields = ['question', 'answer']
    list_filter = ['order']
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'order')
        }),
    )

    def answer_preview(self, obj):
        return obj.answer[:50] + '...' if len(obj.answer) > 50 else obj.answer
    answer_preview.short_description = 'Ответ (превью)'

class RatingAdmin(admin.ModelAdmin):
    list_display = ['page', 'rating_value', 'review_count', 'item_reviewed']
    search_fields = ['page', 'item_reviewed']
    list_filter = ['page']
    ordering = ['page']
    fieldsets = (
        (None, {
            'fields': ('page', 'rating_value', 'review_count', 'item_reviewed', 'worst_rating')
        }),
    )

class CalculatorOptionAdmin(admin.ModelAdmin):
    list_display = ['option_type', 'name', 'value', 'discount', 'parent']
    search_fields = ['name', 'value', 'discount']
    list_filter = ['option_type']
    ordering = ['option_type', 'name']
    fieldsets = (
        (None, {
            'fields': ('option_type', 'name', 'value', 'discount', 'parent')
        }),
    )

# Регистрируем модели напрямую, без декоратора
custom_admin_site.register(MetaData, MetaDataAdmin)
custom_admin_site.register(HeroSection, HeroSectionAdmin)
custom_admin_site.register(District, DistrictAdmin)
custom_admin_site.register(OrderStep, OrderStepAdmin)
custom_admin_site.register(FormConfig, FormConfigAdmin)
custom_admin_site.register(VideoReview, VideoReviewAdmin)
custom_admin_site.register(Photo, PhotoAdmin)
custom_admin_site.register(Price, PriceAdmin)
custom_admin_site.register(Service, ServiceAdmin)
custom_admin_site.register(WhyChooseUs, WhyChooseUsAdmin)
custom_admin_site.register(FAQ, FAQAdmin)
custom_admin_site.register(Rating, RatingAdmin)
custom_admin_site.register(CalculatorOption, CalculatorOptionAdmin)
