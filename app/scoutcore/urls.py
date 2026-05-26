from django.contrib import admin
from django.urls import path, include  # Додаємо include сюди

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("scout.urls")),
]
