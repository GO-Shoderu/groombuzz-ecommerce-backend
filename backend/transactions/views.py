from rest_framework import viewsets, permissions
from .models import Booking, Payment
from .serializers import BookingSerializer, PaymentSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("service", "client").all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("booking").all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
