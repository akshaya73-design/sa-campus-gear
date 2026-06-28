from django.contrib import admin
from .models import Product, Category, Cart, Wishlist
from .models import Activity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = [
        'category_name',
        'slug',
        'is_active'
    ]

    list_editable = [
        'is_active'
    ]

    search_fields = [
        'category_name'
    ]

    prepopulated_fields = {
        'slug': ('category_name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'product_title',
        'sku',
        'product_category',
        'price',
        'stock_quantity',
        'stock_status',
        'is_featured',
        'is_active',
        'updated_date'
    ]

    list_editable = [
        'is_featured',
        'is_active'
    ]

    list_filter = [
        'product_category',
        'is_active',
        'is_featured',
        'created_date'
    ]

    search_fields = [
        'product_title',
        'sku'
    ]

    readonly_fields = [
        'created_date',
        'updated_date'
    ]

    ordering = [
        'product_title'
    ]

    fieldsets = (

        ('Product Information', {

            'fields': (
                'product_title',
                'product_slug',
                'sku',
                'product_category'
            )

        }),

        ('Descriptions', {

            'fields': (
                'short_description',
                'detail_description'
            )

        }),

        ('Pricing & Inventory', {

            'fields': (
                'price',
                'stock_quantity'
            )

        }),

        ('Product Image', {

            'fields': (
                'product_image',
            )

        }),

        ('Status', {

            'fields': (
                'is_active',
                'is_featured'
            )

        }),

        ('Dates', {

            'fields': (
                'created_date',
                'updated_date'
            )

        }),

    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = [
        'product',
        'quantity'
    ]

    search_fields = [
        'product__product_title'
    ]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = [
        'product',
        'created_date'
    ]

    search_fields = [
        'product__product_title'
    ]


admin.site.register(Activity)