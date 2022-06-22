from django.contrib import admin
from .models import Product, Size, Color, Image, Brand, Category
# Register your models here.
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Image)
admin.site.register(Brand)
admin.site.register(Category)
