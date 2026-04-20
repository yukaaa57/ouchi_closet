from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from .models import ClothingItem, Category
from django.contrib.auth import get_user_model
from .forms import ClothingItemForm, CategoryForm, ClothingSearchForm

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
        "current_user_owner": user,
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
        "owner_type": "child",
        "tops_category": get_object_or_404(Category, name="トップス"),
        "bottoms_category": get_object_or_404(Category, name="ボトムス"),
        "onepiece_category": get_object_or_404(Category, name="ワンピース"),
        "outer_category": get_object_or_404(Category, name="アウター"),
        "setup_category": get_object_or_404(Category, name="セットアップ"),
        "shoes_category": get_object_or_404(Category, name="シューズ"),
        "accessory_category": get_object_or_404(Category, name="小物"),
        "bag_category": get_object_or_404(Category, name="バッグ"),
        "current_child": child,
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
    
    order = request.GET.get("order", "new")
    
    if order == "old":
        clothes = clothes.order_by("created_at")
    else:
        clothes = clothes.order_by("-created_at")
        
    context = {
        "owner": owner,
        "owner_type": owner_type,
        "clothes": clothes,
        "category_label": category_label,
        "order": order,
        "is_search_result": False,
    }
    
    return render(request, "closet/clothing_list.html", context)

@login_required
def clothing_create(request, owner_type, owner_id):
    if owner_type == "user":
        owner = get_object_or_404(
            User,
            pk=owner_id,
            family=request.user.family
        )
    else:
        owner = get_object_or_404(
            Child,
            pk=owner_id,
            family=request.user.family
        )
    
    if request.method == "POST":
        form = ClothingItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            clothing = form.save(commit=False)
            
            if owner_type == "user":
                clothing.user = owner
            else:
                clothing.child = owner
            
            clothing.save()
            form.save_m2m()
            
            if owner_type == "user":
                return redirect("user_closet", pk=owner_id)
            else:
                return redirect("child_closet", pk=owner_id)    
    else:
        form = ClothingItemForm()
    
    context = {
        "form": form,
        "owner": owner,
        "owner_type": owner_type,
        "category_form": CategoryForm(),
    }
    
    if owner_type == "child":
        context["current_child"] = owner
    else:
        context["current_user_owner"] = owner
    
    return render(request, "closet/clothing_form.html", context)

@login_required
def clothing_update(request, pk):
    clothing = get_object_or_404(ClothingItem, pk=pk)
    
    if clothing.user:
        if clothing.user.family != request.user.family:
            return redirect("home")
        owner = clothing.user
        owner_type = "user"
    else:
        if clothing.child.family != request.user.family:
            return redirect("home")
        owner = clothing.child
        owner_type = "child"
    
    if request.method == "POST":
        form = ClothingItemForm(request.POST, request.FILES, instance=clothing)
        
        if form.is_valid():
            form.save()
            
            if clothing.user:
                return redirect("user_closet", pk=clothing.user.pk)
            else:
                return redirect("child_closet", pk=clothing.child.pk)
    else:
        form = ClothingItemForm(instance=clothing)
        
    context = {
        "form": form,
        "owner": owner,
        "owner_type": owner_type,
        "is_edit": True,
        "clothing": clothing,
        "category_form": CategoryForm(),
    }
    
    return render(request, "closet/clothing_form.html", context)

@login_required
def clothing_detail(request, pk):
    clothing = get_object_or_404(ClothingItem, pk=pk)
    
    if clothing.user:
        if clothing.user.family != request.user.family:
            return redirect("home")
        owner = clothing.user
        owner_type = "user"
    else:
        if clothing.child.family != request.user.family:
            return redirect("home")
        owner = clothing.child
        owner_type = "child"
        
    next_url = request.GET.get("next", "")
    
    context = {
        "clothing": clothing,
        "owner": owner,
        "owner_type": owner_type,
        "next_url": next_url,
    }
    
    return render(request, "closet/clothing_detail.html", context)

@login_required
def clothing_delete(request, pk):
    clothing = get_object_or_404(ClothingItem, pk=pk)
    
    if clothing.user:
        if clothing.user.family != request.user.family:
            return redirect("home")
        owner = clothing.user
        owner_type = "user"
    else:
        if clothing.child.family != request.user.family:
            return redirect("home")
        owner = clothing.child
        owner_type = "child"
    
    if request.method == "POST":
        next_url = request.POST.get("next", "")
        clothing.delete()
        
        if next_url:
            return redirect(next_url)
        
        return redirect("clothing_list", owner_type=owner_type, owner_id=owner.pk, category="all")
    
    return redirect("clothing_detail", pk=clothing.pk)

@login_required
def clothing_search(request, owner_type, owner_id):
    if owner_type == "user":
        owner = get_object_or_404(
            User,
            pk=owner_id,
            family=request.user.family
        )
    else:
        owner = get_object_or_404(
            Child,
            pk=owner_id,
            family=request.user.family
        )
        
    form = ClothingSearchForm()
    
    context = {
        "form": form,
        "owner": owner,
        "owner_type": owner_type,
    }
    
    if owner_type == "child":
        context["current_child"] = owner
    else:
        context["current_user_owner"] = owner
    
    return render(request, "closet/clothing_search.html", context)

@login_required
def clothing_search_results(request, owner_type, owner_id):
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
        
    form = ClothingSearchForm(request.GET or None)
    search_conditions = []
    
    if form.is_valid():
        category = form.cleaned_data.get("category")
        size = form.cleaned_data.get("size")
        color = form.cleaned_data.get("color")
        seasons = form.cleaned_data.get("season")
        wear_status = form.cleaned_data.get("wear_status")
        
        if category:
            clothes = clothes.filter(category=category)
            search_conditions.append(f"{category.name}")
        if size:
            clothes = clothes.filter(size=size)
            search_conditions.append(f"{size}")
        if color:
            clothes = clothes.filter(color=color)
            search_conditions.append(f"{color}")
        if seasons:
            clothes = clothes.filter(seasons__in=seasons).distinct()
            season_names= []
            for season in seasons:
                season_names.append(season.name)
            search_conditions.append(f"・".join(season_names))
        if wear_status:
            clothes = clothes.filter(wear_status=wear_status)
            search_conditions.append(f"{wear_status}")
    
    order = request.GET.get("order", "new")
    
    if order == "old":
        clothes = clothes.order_by("created_at")
    else:
        clothes = clothes.order_by("-created_at")
    
    context = {
        "owner": owner,
        "owner_type": owner_type,
        "clothes": clothes,
        "search_conditions": search_conditions,
        "order": order,
        "is_search_result": True,
        "selected_season_ids": request.GET.getlist("season"),
    }
    
    return render(request, "closet/clothing_list.html", context)

@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        next_url = request.POST.get("next", "")
        
        if form.is_valid():
            form.save()
            
            if next_url:
                return redirect(next_url)
            
            return redirect("home")
    else:
        form = CategoryForm()
        
    context = {
        "form": form,
    }
    
    return render(request, "closet/category_form.html", context)



    
            
    
        


