from rest_framework import viewsets, permissions
from .models import Business, Category, Service
from .serializers import BusinessSerializer, CategorySerializer, ServiceSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related("business", "category").all()
    serializer_class = ServiceSerializer
    filterset_fields = ["category", "business", "is_available"]
    search_fields = ["name", "description", "business__name"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]
