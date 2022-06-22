from django.db import models
from user_accounts.models import User


class Image(models.Model):
    image = models.ImageField(upload_to='images/', unique=True)

    def __str__(self):
        return self.image.url


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)
    brandImage = models.ImageField(upload_to='brand_images/')


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    categoryImage = models.ImageField(upload_to='category_images/')


class Color(models.Model):
    colorName = models.CharField(max_length=100, unique=True)
    hexColor = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.colorName


class Size(models.Model):
    sex_choices = (
        ("Men's", 'mens'),
        ("Women's", 'womens'),
    )

    size = models.FloatField(unique=True)
    country = models.CharField(max_length=50)
    sex = models.CharField(max_length=50, choices=sex_choices)

    def __str__(self):
        return f'{self.size} for {self.sex} From {self.country} Country'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    actualPrice = models.FloatField()
    sellingPrice = models.FloatField()
    rating = models.IntegerField(default=0)
    relatedBrand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    relatedCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    addedBy = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mainImage = models.OneToOneField(Image, unique=True, on_delete=models.DO_NOTHING)
    otherImages = models.ManyToManyField(Image, related_name='product_images')
    sizes = models.ManyToManyField(Size, related_name='product_size')
    colors = models.ManyToManyField(Color, related_name='product_color')

    def __str__(self):
        return self.name
