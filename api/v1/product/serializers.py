from rest_framework import serializers
from apps.product.models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        if obj.parent:
            return CategorySerializer(obj.parent).data
        return None

    class Meta:
        model = Category
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj: Product):
        main_image: Image = obj.images.filter(status="M").first()
        if main_image:
            return self.context['request'].build_absolute_uri(main_image.source.url)
        return None

    class Meta:
        model = Product
        fields = ["id", "name_uz", "name_ru", "price", "price_type", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
