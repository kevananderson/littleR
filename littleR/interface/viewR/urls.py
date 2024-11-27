"""Defines URL patterns for viewR."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
