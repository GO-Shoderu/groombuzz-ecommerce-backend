from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Business(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)

    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city", "area"]),
        ]

    def __str__(self):
        return self.name

