from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = router.urls
