from django.db import models
import uuid


class Wallet(models.Model):
    """Wallet model that have uuid instead of id, and balance fields"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)



