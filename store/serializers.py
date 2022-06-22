from rest_framework.serializers import ModelSerializer
from .models import Product, Category, Color, Size, Brand, Image


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    relatedBrand = BrandSerializer()
    relatedCategory = CategorySerializer()
    mainImage = ImageSerializer()
    colors = ColorSerializer(many=True)
    otherImages = ImageSerializer(many=True)
    sizes = SizeSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'sellingPrice',
            'rating',
            'relatedBrand',
            'relatedCategory',
            'mainImage',
            'otherImages',
            'sizes',
            'colors'
        ]
