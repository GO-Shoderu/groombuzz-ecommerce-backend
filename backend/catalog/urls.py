from rest_framework.routers import DefaultRouter
from .views import BusinessViewSet, CategoryViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"businesses", BusinessViewSet)
router.register(r"services", ServiceViewSet)

urlpatterns = router.urls
