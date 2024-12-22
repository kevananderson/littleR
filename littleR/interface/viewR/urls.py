"""Defines URL patterns for viewR."""

from django.urls import path

from . import views
from . import ajax_views

app_name = "viewR"
urlpatterns = [
    path("", views.index, name="index"),
    path("req/<str:req_id>", views.detail, name="detail"),
    path("ajax_req_text/<str:req_id>", ajax_views.req_text, name="ajax_req_text"),
]
