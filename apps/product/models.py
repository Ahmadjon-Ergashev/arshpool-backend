from django.db import models

# Create your models here.

class Category(models.Model):
    STATUS_CHOICES = (
        ("M", "Main"),
        ("A", "Additional"),
    )
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category/")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", related_name="childrens", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name_uz


class Image(models.Model):
    STATUS_CHOICES = (
        ("M", "Main"),
        ("A", "Additional"),
    )
    source = models.ImageField(upload_to="product/")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image - {self.pk}"


class Product(models.Model):
    PRICE_TYPE_CHOICES = (
        ("USD", "US Dollar"),
        ("UZS", "Uzbekistan Sum"),
    )
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=3, choices=PRICE_TYPE_CHOICES)
    images = models.ManyToManyField(Image, related_name="products", blank=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show_landing = models.BooleanField(default=False)

    def __str__(self):
        return self.name_uz