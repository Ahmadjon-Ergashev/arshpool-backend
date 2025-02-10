from rest_framework.routers import DefaultRouter
from api.v1.views.product import CategoryViewSet, ProductViewSet


router = DefaultRouter()
router.register(r"product/category", CategoryViewSet)
router.register(r"product/products", ProductViewSet, basename="product")

urlpatterns = router.urls
