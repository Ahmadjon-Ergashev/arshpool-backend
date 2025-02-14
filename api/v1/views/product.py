from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.product.models import Category, Product
from api.v1.serializers.product import CategorySerializer, ProductSerializer, ProductListSerializer


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=["get"])
    def landing(self, request, pk=None):
        products = Product.objects.filter(show_landing=True)
        serializer = ProductListSerializer(products, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class CategoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = "slug"
    # lookup_url_kwarg = "slug"
    
    def get_queryset(self):
        if self.action == "list":
            return Category.objects.filter(parent=None)
        return super().get_queryset()
