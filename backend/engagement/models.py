from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Review(TimeStampedModel):
    booking = models.OneToOneField(
        "transactions.Booking",
        on_delete=models.CASCADE,
        related_name="review",
    )
    business = models.ForeignKey(
        "catalog.Business",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["rating"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Review({self.rating}/5 by {self.client})"


class Message(TimeStampedModel):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    business = models.ForeignKey(
        "catalog.Business",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    message_body = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Message({self.sender} → {self.recipient})"
