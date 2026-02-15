from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Review, Message
from .serializers import ReviewSerializer, MessageSerializer
from transactions.models import Booking


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Review.objects.select_related("booking", "business", "client").all()

        return Review.objects.select_related("booking", "business", "client").filter(
            Q(client=user) | Q(business__owner=user)
        ).distinct()

    def perform_create(self, serializer):
        booking = serializer.validated_data["booking"]

        if booking.client != self.request.user:
            raise PermissionDenied("You can only review your own bookings.")

        if booking.status != Booking.Status.COMPLETED:
            raise ValidationError("You can only review a completed booking.")

        if hasattr(booking, "review"):
            raise ValidationError("This booking already has a review.")

        serializer.save(
            client=self.request.user,
            business=booking.service.business,
        )


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Message.objects.select_related("sender", "recipient", "business").all()

        return Message.objects.select_related("sender", "recipient", "business").filter(
            Q(sender=user) | Q(recipient=user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
