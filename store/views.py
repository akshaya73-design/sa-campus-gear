# Updated views.py (Partially enhanced)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product, Category, Cart, Wishlist, Activity
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


def home(request):

    categories = Category.objects.filter(is_active=True)

    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    )

    search = request.GET.get("search")

    if search:

        products = Product.objects.filter(

            Q(product_title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(sku__icontains=search),

            is_active=True

        )

    context = {

        "categories": categories,

        "products": products,

        "search": search,

        "cart_count": Cart.objects.count(),

        "wishlist_count": Wishlist.objects.count(),

    }

    return render(
        request,
        "home.html",
        context
    )

def category_products(request, slug):

    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(
        product_category=category,
        is_active=True
    )

    sort = request.GET.get("sort")

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "latest":
        products = products.order_by("-created_date")

    return render(request, "category.html", {
        "category": category,
        "categories": categories,
        "products": products,
        "product_count": products.count(),
        "selected_sort": sort,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count()
    })

def product_detail(request, slug):
    product=get_object_or_404(Product,product_slug=slug,is_active=True)
    related=Product.objects.filter(product_category=product.product_category,is_active=True).exclude(id=product.id)[:4]
    return render(request,"product_detail.html",{
        "product":product,
        "related_products":related,
        "categories":Category.objects.filter(is_active=True),
        "cart_count":Cart.objects.count(),
        "wishlist_count":Wishlist.objects.count()
    })

def add_to_cart(request, product_id):
    product=get_object_or_404(Product,id=product_id)

    if product.stock_quantity==0:
        messages.error(request,"Product is Out Of Stock.")
        return redirect("product_detail",slug=product.product_slug)

    cart=Cart.objects.filter(product=product).first()

    if cart:
        if cart.quantity>=product.stock_quantity:
            messages.warning(request,"Maximum available stock reached.")
        else:
            cart.quantity+=1
            cart.save()
            messages.success(request,"Cart updated.")
    else:
        Cart.objects.create(product=product,quantity=1)
        messages.success(request,"Product added to cart.")
    request.session["continue_url"] = request.META.get("HTTP_REFERER")
    return redirect("cart")

def cart_view(request):
    items = Cart.objects.all()
    total = sum(i.product.price * i.quantity for i in items)

    return render(request, "cart.html", {
        "cart_items": items,
        "total": total,
        "continue_url": request.session.get("continue_url", "/"),
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

def remove_from_cart(request,cart_id):
    Cart.objects.filter(id=cart_id).delete()
    messages.success(request,"Item removed.")
    return redirect("cart")

def increase_quantity(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)

    if item.quantity < item.product.stock_quantity:
        item.quantity += 1
        item.save()
    else:
        messages.warning(request, "No more stock available.")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/cart/"))

def decrease_quantity(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/cart/"))

def add_to_wishlist(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    Wishlist.objects.get_or_create(product=product)
    messages.success(request,"Added to wishlist.")
    request.session["continue_url"] = request.META.get("HTTP_REFERER")
    return redirect("wishlist")

def wishlist_view(request):
    return render(request,"wishlist.html",{
        "wishlist_items":Wishlist.objects.all(),
        "categories":Category.objects.filter(is_active=True),
        "cart_count":Cart.objects.count(),
        "wishlist_count":Wishlist.objects.count()
    })

def remove_from_wishlist(request,wishlist_id):
    Wishlist.objects.filter(id=wishlist_id).delete()
    messages.success(request,"Removed from wishlist.")
    return redirect("wishlist")


def checkout(request):

    cart_items = Cart.objects.all()

    for item in cart_items:

        product = item.product

        if product.stock_quantity >= item.quantity:

            product.stock_quantity -= item.quantity

            product.sale_count += item.quantity

            product.save()

            Activity.objects.create(
                activity=f"🛒 {product.product_title} sold ({item.quantity} items)"
            )
        else:

            messages.error(
                request,
                f"{product.product_title} does not have enough stock."
            )

            return redirect("cart")

    Cart.objects.all().delete()

    messages.success(
        request,
        "Order Placed Successfully!"
    )

    return redirect("home")

@staff_member_required
@require_POST
def restock_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    quantity = request.POST.get("quantity")

    try:

        quantity = int(quantity)

        if quantity > 0:

            product.stock_quantity += quantity

            product.save()

            Activity.objects.create(
                 activity=f"➕ {quantity} {product.product_title} restocked"
            )

            messages.success(
                request,
                f"{quantity} items added successfully."
            )

        else:

            messages.error(
                request,
                "Quantity must be greater than zero."
            )

    except ValueError:

        messages.error(
            request,
            "Invalid quantity."
        )

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@staff_member_required
def inventory_dashboard(request):

    products = Product.objects.all().order_by("product_title")

    search = request.GET.get("search", "").strip()

    if search:
        products = products.filter(
            product_title__icontains=search
    )

    status = request.GET.get("status")

    if status == "stock":
        products = products.filter(stock_quantity__gt=5)

    elif status == "low":
        products = products.filter(
            stock_quantity__gt=0,
            stock_quantity__lte=5
        )

    elif status == "out":
        products = products.filter(stock_quantity=0)

    # ✅ ALWAYS define stats here (outside conditions)
    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    in_stock = Product.objects.filter(stock_quantity__gt=5).count()

    low_stock = Product.objects.filter(
        stock_quantity__gt=0,
        stock_quantity__lte=5
    ).count()

    out_of_stock = Product.objects.filter(stock_quantity=0).count()

    health = (
    (in_stock * 100)
    + (low_stock * 60)
    + (out_of_stock * 20)
)
    total = total_products * 100

    health_percentage = round(health / total)

    top_products = Product.objects.order_by(
    "-sale_count"
    )[:5]
    
    activities = Activity.objects.all()[:5]

    low_stock_products = Product.objects.filter(
    stock_quantity__gt=0,
    stock_quantity__lte=5
)

    out_stock_products = Product.objects.filter(
        stock_quantity=0
    )

    continue_url = request.session.get("continue_url", "/")

    context = {
        "products": products,
        "total_products": total_products,
        "total_categories": total_categories,
        "in_stock": in_stock,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "selected_status": status,
        "health_percentage": health_percentage,
        "top_products": top_products,
        "low_stock_products": low_stock_products,
        "out_stock_products": out_stock_products,
        "activities": activities,
        "search": search,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
        "categories": Category.objects.filter(is_active=True)
    }



    return render(
        request,
        "inventory_dashboard.html",
        context
    )