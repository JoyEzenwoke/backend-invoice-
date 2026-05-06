# invoices\serializers.py
from rest_framework import serializers
from .models import Invoice
from items.models import Item
from items.serializers import ItemSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    # CREATE INVOICE
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        invoice = Invoice.objects.create(**validated_data)
        return self._save_items(invoice, items_data)

    # UPDATE INVOICE
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # update invoice fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # replace items if provided
        if items_data is not None:
            instance.items.all().delete()
            self._save_items(instance, items_data)

        return instance

    # HANDLE ITEM CREATION + TOTAL
    def _save_items(self, invoice, items_data):
        total = 0

        for item_data in items_data:
            item = Item.objects.create(
                invoice=invoice,
                name=item_data['name'],
                quantity=item_data['quantity'],
                price=item_data['price'],
            )

            item.total = item.quantity * item.price
            item.save()

            total += item.total

        invoice.total = total
        invoice.save()

        return invoice

    # FIX JSON SERIALIZATION (IMPORTANT)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items'] = ItemSerializer(instance.items.all(), many=True).data
        return data