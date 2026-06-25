from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug', 'is_active']
    list_editable = ['is_active']
    search_fields = ['category_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'product_title',
        'product_slug',
        'product_category',
        'price',
        'is_active',
        'is_featured',
        'updated_date'
    ]

    list_editable = ['is_active', 'is_featured']
    list_filter = ['product_category', 'is_active', 'is_featured']
    search_fields = ['product_title', 'sku']