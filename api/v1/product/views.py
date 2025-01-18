from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from apps.product.models import Category, Product
from .serializers import CategorySerializer, ProductSerialier


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerialier


class CategoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"