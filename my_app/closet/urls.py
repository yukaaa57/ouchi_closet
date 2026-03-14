from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:pk>/", views.user_closet, name="user_closet"),
    path("child/<int:pk>/", views.child_closet, name="child_closet"),
    path("<str:owner_type>/<int:owner_id>/all/", views.clothing_list_all, name="clothing_list_all"),
    path("<str:owner_type>/<int:owner_id>/category/<int:category_id>/", views.clothing_list, name="clothing_list")
]
