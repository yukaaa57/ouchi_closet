from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:pk>/", views.user_closet, name="user_closet"),
    path("child/<int:pk>/", views.child_closet, name="child_closet"),
]
