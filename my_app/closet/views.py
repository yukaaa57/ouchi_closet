from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from .models import ClothingItem, Category
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def user_closet(request, pk):
    user = get_object_or_404(
        User,
        pk=pk,
        family=request.user.family
    )
    
    context = {
        "owner": user,
        "owner_type": "user",
        "tops_category": get_object_or_404(Category, name="トップス"),
        "bottoms_category": get_object_or_404(Category, name="ボトムス"),
        "onepiece_category": get_object_or_404(Category, name="ワンピース"),
        "outer_category": get_object_or_404(Category, name="アウター"),
        "setup_category": get_object_or_404(Category, name="セットアップ"),
        "shoes_category": get_object_or_404(Category, name="シューズ"),
        "accessory_category": get_object_or_404(Category, name="小物"),
        "bag_category": get_object_or_404(Category, name="バッグ"),
    }
    
    return render(request, "closet/user_closet.html", context)
    
@login_required
def child_closet(request, pk):
    child = get_object_or_404(
        Child,
        pk=pk,
        family=request.user.family
    )
    
    context = {
        "owner": child,
        "owner_type": "childr",
        "tops_category": get_object_or_404(Category, name="トップス"),
        "bottoms_category": get_object_or_404(Category, name="ボトムス"),
        "onepiece_category": get_object_or_404(Category, name="ワンピース"),
        "outer_category": get_object_or_404(Category, name="アウター"),
        "setup_category": get_object_or_404(Category, name="セットアップ"),
        "shoes_category": get_object_or_404(Category, name="シューズ"),
        "accessory_category": get_object_or_404(Category, name="小物"),
        "bag_category": get_object_or_404(Category, name="バッグ"),
    }
    
    return render(request, "closet/child_closet.html", context)

@login_required
def clothing_list(request, owner_type, owner_id, category):
    
    if owner_type == "user":
        owner = get_object_or_404(
            User,
            pk=owner_id,
            family=request.user.family
        )
        clothes = ClothingItem.objects.filter(user=owner)
    else:
        owner = get_object_or_404(
            Child,
            pk=owner_id,
            family=request.user.family
        )
        clothes = ClothingItem.objects.filter(child=owner)
        
    if category != "all":
        category_obj = get_object_or_404(Category, pk=category)
        clothes = clothes.filter(category=category_obj)
        category_label = category_obj.name
    else:
        category_label = "すべて"
    
    order = request.GET.get("oder", "new")
    
    if order == "old":
        clothes = clothes.order_by("created_at")
    else:
        clothes = clothes.order_by("-created_at")
        
    context = {
        "owner": owner,
        "owner_type": owner_type,
        "clothes": clothes,
        "category/label": category_label,
        "order": order,
    }
    
    return render(request, "closet/clothing_list.html", context)

