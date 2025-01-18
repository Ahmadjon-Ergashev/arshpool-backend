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


class ProductSerialier(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
