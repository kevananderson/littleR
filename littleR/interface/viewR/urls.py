"""Defines URL patterns for viewR."""

from django.urls import path

from . import views

app_name = "viewR"
urlpatterns = [
    path("", views.index, name="index"),
]
