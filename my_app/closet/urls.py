from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:pk>/", views.user_closet, name="user_closet"),
    path("child/<int:pk>/", views.child_closet, name="child_closet"),
    path("<str:owner_type>/<int:owner_id>/create/", views.clothing_create, name="clothing_create"),
    path("<str:owner_type>/<str:owner_id>/search", views.clothing_search, name="clothing_search"),
    path("<str:owner_type>/<str:owner_id>/search/results", views.clothing_search_results, name="clothing_search_results"),
    path("category/create", views.category_create, name="category_create"),
    path("item/<int:pk>", views.clothing_detail, name="clothing_detail"),
    path("item/<int:pk>/edit/", views.clothing_update, name="clothing_update"),
    path("item/<int:pk>/delete", views.clothing_delete, name="clothing_delete"),
    path("category/setting/", views.category_setting, name="category_setting"),
    path("category/<int:pk>/update/", views.category_update, name="category_update"),
    path("<str:owner_type>/<int:owner_id>/<str:category>/", views.clothing_list, name="clothing_list"),
]
