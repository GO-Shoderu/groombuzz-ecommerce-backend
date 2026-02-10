from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELED = "canceled", "Canceled"
        COMPLETED = "completed", "Completed"

    service = models.ForeignKey(
        "catalog.Service",
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        indexes = [
            models.Index(fields=["scheduled_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Booking({self.client} → {self.service} at {self.scheduled_at})"

