from rest_framework import serializers
from apps.product.models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    childrens = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_childrens(self, obj: Category):
        if obj.childrens.exists():
            return CategorySerializer(obj.childrens, many=True, context=self.context).data
        return None
    
    def get_products(self, obj: Category):
        if obj.products.exists():
            return ProductListSerializer(obj.products, many=True, context=self.context).data
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
