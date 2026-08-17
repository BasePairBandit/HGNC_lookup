from django.urls import path
from hgnc_lookup_app import views

urlpatterns = [
    path("", views.search_gene, name="search"),
]