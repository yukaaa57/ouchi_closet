from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:owner_id>/", views.outfit_list, {"owner_type": "user"}, name="user_outfit_list"),
    path("child/<int:owner_id>/", views.outfit_list, {"owner_type": "child"}, name="child_outfit_list"),
    path("user/<int:owner_id>/favorite/", views.favorite_outfit_list, {"owner_type": "user"}, name="user_favorite_outfit_list"),
    path("child/<int:owner_id>/favorite/", views.favorite_outfit_list, {"owner_type": "child"}, name="child_favorite_outfit_list"),
    path("user/<int:owner_id>/create/<int:outfit_type>/", views.outfit_create, {"owner_type": "user"}, name="user_outfit_create"),
    path("child/<int:owner_id>/create/<int:outfit_type>/", views.outfit_create, {"owner_type": "child"}, name="child_outfit_create"),
    path("item/<int:pk>/", views.outfit_detail, name="outfit_detail"),
    path("item/<int:pk>/edit/", views.outfit_update, name="outfit_update"),
    path("item/<int:pk>/delete/", views.outfit_delete, name="outfit_delete"),
    path("item/image/<int:pk>/delete", views.outfit_image_delete, name="outfit_image_delete"),
    path("item/<int:pk>/favorite/", views.outfit_toggle_favorite, name="outfit_toggle_favorite"),
    path("item/<int:pk>/clothing-search", views.clothing_item_search, name="clothing_item_search"),
]
