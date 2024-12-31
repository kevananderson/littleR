"""Defines URL patterns for viewR."""

from django.urls import path

from . import views
from . import ajax_view

app_name = "viewR"
urlpatterns = [
    path("", views.index, name="index"),
    path("req/<str:req_id>", views.detail, name="detail"),
    path("ajax_req_path/<str:req_id>", ajax_view.req_path, name="ajax_req_path"),
    path("ajax_req_text/<str:req_id>", ajax_view.req_text, name="ajax_req_text"),
    path("ajax_delete_req_label/<str:req_id>", ajax_view.delete_req_label, name="ajax_delete_req_label"),
    path("ajax_add_req_label/<str:req_id>", ajax_view.add_req_label, name="ajax_add_req_label"),
    path("ajax_delete_req_relation/<str:req_id>", ajax_view.delete_req_relation, name="ajax_delete_req_relation"),
    path("ajax_add_req_relation/<str:req_id>", ajax_view.add_req_relation, name="ajax_add_req_relation"),
]
