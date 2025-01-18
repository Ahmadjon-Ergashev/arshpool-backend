from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet


router = DefaultRouter()
router.register(r"category", CategoryViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = router.urls
