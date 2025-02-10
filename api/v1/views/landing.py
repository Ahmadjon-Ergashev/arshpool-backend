from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from apps.landing.models import Project
from apps.product.models import Product
from api.v1.serializers.product import ProductListSerializer
from api.v1.serializers.landing import ProjectSerialier


class ProjectViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerialier
    # lookup_field = "slug"
    # lookup_url_kwarg = "slug"
