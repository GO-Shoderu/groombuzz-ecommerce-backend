from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Booking, Payment
from .serializers import BookingSerializer, PaymentSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.select_related("service", "client", "service__business").all()

        return Booking.objects.select_related("service", "client", "service__business").filter(
            Q(client=user) | Q(service__business__owner=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.select_related("booking", "booking__service", "booking__service__business").all()

        return Payment.objects.select_related("booking", "booking__service", "booking__service__business").filter(
            Q(booking__client=user) | Q(booking__service__business__owner=user)
        ).distinct()
