from django.db import models
from decimal import Decimal
#Account model
class Account(models.Model):
    phone = models.CharField(max_length=13, unique=True)  # Phone number must be unique
    username = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.phone}) - Balance: {self.balance}"
