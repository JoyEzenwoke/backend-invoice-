# invoices\views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer


# ✅ LIST + CREATE + FILTER
class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        queryset = Invoice.objects.all()
        status_param = self.request.query_params.get('status')

        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        return queryset


# ✅ DETAIL + UPDATE + DELETE + LOCK LOGIC
class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == 'paid':
            return Response(
                {"error": "Paid invoices cannot be modified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == 'paid':
            return Response(
                {"error": "Paid invoices cannot be deleted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)