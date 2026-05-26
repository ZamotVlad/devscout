from django.contrib import admin
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "source", "pub_date")

    list_filter = ("source", "pub_date")

    search_fields = ("title", "company", "description")

    ordering = ("-pub_date",)

    list_per_page = 25
