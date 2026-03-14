from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from .models import ClothingItem, Category

@login_required
def user_closet(request, pk):
    user = get_object_or_404(
        User,
        pk=pk,
        family=request.user.family
    )
    
    categories = Category.objects.all()
    
    context = {
        "owner": user,
        "owner_type": "user",
        "categories": categories,
    }
    
    return render(request, "closet/user_closet.html", context)
    
@login_required
def child_closet(request, pk):
    child = get_object_or_404(
        Child,
        pk=pk,
        family=request.user.family
    )
    
    categories = Category.objects.all()
    
    context = {
        "owner": child,
        "owner_type": "childr",
        "categories": categories,
    }
    
    return render(request, "closet/child_closet.html", context)

@login_required
def clothing_list(request, owner_type, owner_id, category_id):
    
    category = get_object_or_404(Category, pk=category_id)
    
    if owner_type == "user":
        clothes = ClothingItem.objects.filter(
            user_id=owner_id,
            category=category
        )
    else:
        clothes = ClothingItem.objects.filter(
            child_id=owner_id,
            category=category
        )
    
    order = request.GET.get("oder", "new")
    
    if order == "old":
        clothes = clothes.order_by("created_at")
    else:
        clothes = clothes.order_by("-created_at")
        
    context = {
        "clothes": clothes,
        "category": category,
    }
    
    return render(request, "closet/clothing_list.html", context)

