from django.db import models
from django.utils.text import slugify


class Category(models.Model):

    category_name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        max_length=120,
        blank=True
    )

    category_image = models.ImageField(
        upload_to='category/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def save(self, *args, **kwargs):

        self.slug = slugify(
            self.category_name
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.category_name


class Product(models.Model):

    product_title = models.CharField(
        max_length=200
    )

    product_slug = models.SlugField(
        max_length=250,
        blank=True
    )

    sku = models.CharField(
        max_length=100
    )

    short_description = models.TextField()

    detail_description = models.TextField()

    product_image = models.ImageField(
        upload_to='product/'
    )

    price = models.IntegerField()

    product_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_date = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        self.product_slug = slugify(
            self.product_title
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.product_title


class Cart(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    def __str__(self):

        return self.product.product_title


class Wishlist(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.product.product_title