from rest_framework import viewsets, permissions
from .models import Business, Category, Service
from .serializers import BusinessSerializer, CategorySerializer, ServiceSerializer
from common.permissions import IsStaffOrReadOnly
from rest_framework.exceptions import PermissionDenied

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related("business", "category").all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filterset_fields = ["category", "business", "is_available"]
    search_fields = ["name", "description", "business__name"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        business = serializer.validated_data["business"]
        if not (self.request.user.is_staff or business.owner == self.request.user):
            raise PermissionDenied("You can only create services for your own business.")
        serializer.save()

    def perform_update(self, serializer):
        business = serializer.instance.business
        if not (self.request.user.is_staff or business.owner == self.request.user):
            raise PermissionDenied("You can only update services for your own business.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.business.owner == self.request.user):
            raise PermissionDenied("You can only delete services for your own business.")
        instance.delete()