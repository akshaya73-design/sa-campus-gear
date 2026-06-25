from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'category/<slug:slug>/',
        views.category_products,
        name='category_products'
    ),

    path(
        'product/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    path(
        'remove-from-cart/<int:cart_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'increase-quantity/<int:cart_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease-quantity/<int:cart_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    # =========================
    # WISHLIST
    # =========================

    path(
        'add-to-wishlist/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'wishlist/',
        views.wishlist_view,
        name='wishlist'
    ),

    path(
        'remove-from-wishlist/<int:wishlist_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),

]