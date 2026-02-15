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

    def validate(self, attrs):
        amount = attrs.get("amount")
        if amount is not None and amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0."})
        return attrs

    def create(self, validated_data):
        from django.utils import timezone

        if validated_data.get("payment_status") == "completed" and not validated_data.get("payment_date"):
            validated_data["payment_date"] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        from django.utils import timezone

        new_status = validated_data.get("payment_status")
        if new_status == "completed" and instance.payment_date is None:
            validated_data["payment_date"] = timezone.now()
        return super().update(instance, validated_data)
