from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = router.urls
