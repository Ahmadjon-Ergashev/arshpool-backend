from rest_framework.routers import DefaultRouter
from api.v1.views.landing import ProjectViewSet


router = DefaultRouter()
router.register(r"landing/projects", ProjectViewSet)

urlpatterns = router.urls
