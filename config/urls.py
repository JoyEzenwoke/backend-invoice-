# config\urls.py
from django.contrib import admin
from django.urls import path, include

# Swagger imports
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/invoices/', include('invoices.urls')),

    #  Swagger schema (raw JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    #  Swagger UI (interactive docs)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]