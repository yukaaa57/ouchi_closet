from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:owner_id>/", views.outfit_list, {"owner_type": "user"}, name="user_outfit_list"),
    path("child/<int:owner_id>/", views.outfit_list, {"owner_type": "child"}, name="child_outfit_list"),
    path("item/<imt:pk>/favorite/", views.outfit_toggle_favorite, name="outfit_toggle_favorite"),
]
