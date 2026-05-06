# items\models.py

from django.db import models
from invoices.models import Invoice

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # calculate item total
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name