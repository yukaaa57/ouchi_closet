from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:owner_id>/", views.outfit_list, {"owner_type": "user"}, name="user_outfit_list"),
    path("child/<int:owner_id>/", views.outfit_list, {"owner_type": "child"}, name="child_outfit_list"),
    path("item/<int:pk>/", views.outfit_detail, name="outfit_detail"),
    path("item/<int:pk>/edit/", views.outfit_update, name="outfit_update"),
    path("item/<int:pk>/favorite/", views.outfit_toggle_favorite, name="outfit_toggle_favorite"),
]
