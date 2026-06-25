from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category, Cart, Wishlist


def home(request):

    categories = Category.objects.filter(
        is_active=True
    )

    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    )

    cart_count = Cart.objects.count()

    wishlist_count = Wishlist.objects.count()

    context = {
        'categories': categories,
        'products': products,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }

    return render(
        request,
        'home.html',
        context
    )


def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    categories = Category.objects.filter(
        is_active=True
    )

    products = Product.objects.filter(
        product_category=category,
        is_active=True
    )

    sort = request.GET.get('sort')

    if sort == 'price_low':
        products = products.order_by('price')

    elif sort == 'price_high':
        products = products.order_by('-price')

    elif sort == 'latest':
        products = products.order_by('-created_date')

    cart_count = Cart.objects.count()

    wishlist_count = Wishlist.objects.count()

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'product_count': products.count(),
        'selected_sort': sort,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }

    return render(
        request,
        'category.html',
        context
    )


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        product_slug=slug,
        is_active=True
    )

    categories = Category.objects.filter(
        is_active=True
    )

    related_products = Product.objects.filter(
        product_category=product.product_category,
        is_active=True
    ).exclude(
        id=product.id
    )[:4]

    cart_count = Cart.objects.count()

    wishlist_count = Wishlist.objects.count()

    context = {
        'product': product,
        'categories': categories,
        'related_products': related_products,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }

    return render(
        request,
        'product_detail.html',
        context
    )

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart_item = Cart.objects.filter(
        product=product
    ).first()

    if cart_item:

        cart_item.quantity += 1

        cart_item.save()

    else:

        Cart.objects.create(
            product=product,
            quantity=1
        )

    return redirect('cart')


def cart_view(request):

    cart_items = Cart.objects.all()

    total = 0

    for item in cart_items:

        total += item.product.price * item.quantity

    cart_count = Cart.objects.count()

    wishlist_count = Wishlist.objects.count()

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }

    return render(
        request,
        'cart.html',
        context
    )


def remove_from_cart(request, cart_id):

    cart_item = Cart.objects.get(
        id=cart_id
    )

    cart_item.delete()

    return redirect('cart')


def increase_quantity(request, cart_id):

    cart_item = Cart.objects.get(
        id=cart_id
    )

    cart_item.quantity += 1

    cart_item.save()

    return redirect('cart')


def decrease_quantity(request, cart_id):

    cart_item = Cart.objects.get(
        id=cart_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect('cart')


# =========================
# WISHLIST
# =========================

def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item = Wishlist.objects.filter(
        product=product
    ).first()

    if not wishlist_item:

        Wishlist.objects.create(
            product=product
        )

    return redirect('wishlist')


def wishlist_view(request):

    wishlist_items = Wishlist.objects.all()

    categories = Category.objects.filter(
        is_active=True
    )

    cart_count = Cart.objects.count()

    wishlist_count = Wishlist.objects.count()

    context = {
        'wishlist_items': wishlist_items,
        'categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }

    return render(
        request,
        'wishlist.html',
        context
    )


def remove_from_wishlist(request, wishlist_id):

    wishlist_item = Wishlist.objects.get(
        id=wishlist_id
    )

    wishlist_item.delete()

    return redirect('wishlist')