from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Category, Image, Product

from pprint import pprint

# Register your models here.

class ImageGalleryWidget(forms.CheckboxSelectMultiple):
    template_name = 'widgets/image_gallery.html'

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        if hasattr(value, 'value'):
            value = value.value
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        try:
            image = Image.objects.get(pk=value)
            option['label'] = format_html(
                '<img src="{}" style="width: 100px; height: 100px; display: block; margin: auto; object-fit: cover;">{}',
                image.source.url, label
            )
        except Image.DoesNotExist:
            option['label'] = label
        return option
    

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'images': ImageGalleryWidget(),
        }


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name_uz", "name_ru"]
    list_display = ["name_uz", "name_ru", "parent"]
    list_filter = ["parent"]
    list_display_links = ["name_uz"]


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    search_fields = ["name_uz", "name_ru"]
    list_display = ["name_uz", "name_ru", "price", "category"]
    list_filter = ["category"]
    list_editable = ["price"]
    readonly_fields = ["created_at", "updated_at"]
    list_display_links = ["name_uz"]

    autocomplete_fields = ["category"]

    fieldsets = (
        (
            _("Uzbek"),
            {
                "fields": ["name_uz", "description_uz"],
            },
        ),
        (
            _("Russian"),
            {
                "fields": ["name_ru", "description_ru"],
            },
        ),
        (
            "Date information",
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
        (
            None,
            {
                "fields": (
                    "price",
                    "price_type",
                    "category",
                    "in_stock",
                    "images",
                )
            },
        ),
    )

    class Media:
        css = {
            'all': ('css/image-gallery.css',),
        }
        js = ('js/image-gallery.js',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Image)
admin.site.register(Product, ProductAdmin)
