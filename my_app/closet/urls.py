from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:pk>/", views.user_closet, name="user_closet"),
    path("child/<int:pk>/", views.child_closet, name="child_closet"),
    path("<str:owner_type>/<int:owner_id>/<str:category>/", views.clothing_list, name="clothing_list"),
    path("<str:owner_type>/<int:owner_id>/create/", views.clothing_create, name="clothing_create"),
]
