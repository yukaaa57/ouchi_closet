from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:owner_id>/", views.outfit_list, {"owner_type": "user"}, name="user_outfit_list"),
    path("child/<int:owner_id>/", views.outfit_list, {"owner_type": "child"}, name="child_outfit_list"),
    path("user/<int:owner_id>/favorite/", views.favorite_outfit_list, {"owner_type": "user"}, name="user_favorite_outfit_list"),
    path("child/<int:owner_id>/favorite/", views.favorite_outfit_list, {"owner_type": "child"}, name="child_favorite_outfit_list"),
    path("<str:owner_type>/<int:owner_id>/select/", views.outfit_select, name="outfit_select"),
    path("user/<int:owner_id>/create/<int:outfit_type>/", views.outfit_create, {"owner_type": "user"}, name="user_outfit_create"),
    path("child/<int:owner_id>/create/<int:outfit_type>/", views.outfit_create, {"owner_type": "child"}, name="child_outfit_create"),
    path("user/<int:owner_id>/create/clothing_search/", views.clothing_item_search_create, {"owner_type": "user"}, name="user_clothing_item_search_create" ),
    path("child/<int:owner_id>/create/clothing_search/", views.clothing_item_search_create, {"owner_type": "child"}, name="child_clothing_item_search_create" ),
    path("item/<int:pk>/", views.outfit_detail, name="outfit_detail"),
    path("item/<int:pk>/edit/", views.outfit_update, name="outfit_update"),
    path("item/<int:pk>/delete/", views.outfit_delete, name="outfit_delete"),
    path("item/image/<int:pk>/delete", views.outfit_image_delete, name="outfit_image_delete"),
    path("item/<int:pk>/favorite/", views.outfit_toggle_favorite, name="outfit_toggle_favorite"),
    path("item/<int:pk>/clothing-search", views.clothing_item_search, name="clothing_item_search"),
    path("nursery/<int:child_id>/create/", views.nursery_item_create, name="nursery_item_create"),
    path("nursery/<int:child_id>/", views.nursery_item_list, name="nursery_item_list"),
    path("nursery/item/<int:item_id>/check/", views.nursery_item_check, name="nursery_item_check"),
    path("nursery/<int:child_id>/reset/<int:item_type>/", views.nursery_item_reset, name="nursery_item_reset"),
]
