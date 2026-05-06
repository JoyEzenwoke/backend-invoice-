# invoices\models.py
from django.db import models
from clients.models import Client

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    invoice_date = models.DateField()
    payment_terms = models.IntegerField(help_text="Days to payment")

    project_description = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.client.name}"