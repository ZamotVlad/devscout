from django.urls import path
from . import views

app_name = "scout"

urlpatterns = [
    path("", views.vacancy_list, name="vacancy_list"),
    path("trigger-parser/<str:site_name>/", views.trigger_parser_view, name="trigger_parser"),
]
