from django.utils import timezone
from rest_framework import serializers
from .models import Booking, Payment


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["client", "created_at", "updated_at"]

    def validate_scheduled_at(self, value):
        # Preventing booking in the past
        if value <= timezone.now():
            raise serializers.ValidationError("scheduled_at must be in the future.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
