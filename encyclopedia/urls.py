from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("search/", views.search, name="search"), #type: ignore 
    path("create/", views.create, name="create_page"), #type: ignore
    path("wiki/<str:title>/edit/", views.edit, name="edit_page"), #type: ignore
    path("successful_save/", views.save, name="save_page"), #type: ignore
    path("random_page/", views.random_page, name="random_page") #type: ignore
]
