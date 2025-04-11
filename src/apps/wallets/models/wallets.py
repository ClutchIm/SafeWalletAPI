from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Wallet(models.Model):
    """Wallet model that have uuid instead of id, and balance fields"""
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def clean(self):
        """Checking is balance are positive"""
        if self.balance < 0:
            raise ValidationError(
                {"detail": "Balance cannot be negative."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # calls clean()
        super().save(*args, **kwargs)
