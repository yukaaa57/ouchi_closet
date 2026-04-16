from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from closet.models import ClothingItem, Category
from .models import Outfit, OutfitImage, OutfitClothingItem, OutfitUrl, NurseryItem
from .forms import OutfitForm, OutfitImageForm, NurseryItemForm

@login_required
def outfit_list(request, owner_type, owner_id):
    if owner_type == "user":
        owner = get_object_or_404(
            User,
            pk=owner_id,
            family=request.user.family
        )
        outfits = Outfit.objects.filter(user=owner)
    else:
        owner = get_object_or_404(
            Child,
            pk=owner_id,
            family=request.user.family
        )
        outfits = Outfit.objects.filter(child=owner)
        
    order = request.GET.get("order", "new")
    
    if order == "old":
        outfits = outfits.order_by("created_at")
    else:
        outfits = outfits.order_by("-created_at")
    
    context = {
        "owner": owner,
        "owner_type": owner_type,
        "outfits": outfits,
        "order": order,
    }
    
    return render(request, "cordinate/outfit_list.html", context)

@login_required
def outfit_toggle_favorite(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    
    if outfit.user:
        if outfit.user.family != request.user.family:
            return redirect("home")
    else:
        if outfit.child.family != request.user.family:
            return redirect("home")
    
    if request.method == "POST":
        outfit.is_favorite = not outfit.is_favorite
        outfit.save()
        
        next_url = request.POST.get("next", "")
        if next_url:
            return redirect(next_url)
    
    return redirect("home")

@login_required
def outfit_create(request, owner_type, owner_id, outfit_type):
    if owner_type == "user":
        owner = get_object_or_404(User, pk=owner_id)
        if owner.family != request.user.family:
            return redirect("home")
    else:
        owner = get_object_or_404(Child, pk=owner_id)
        if owner.family != request.user.family:
            return redirect ("home")
    
    if request.method == "POST":
        form = OutfitForm(request.POST)
        
        if form.is_valid():
            outfit = form.save(commit=False)
            
            if owner_type == "user":
                outfit.user = owner
                outfit.child = None
            else:
                outfit.child = owner
                outfit.user = None
                
            outfit.outfit_type = int(outfit_type)
            
            if int(outfit_type) == 1:
                outfit.is_favorite = True
                
            outfit.save()
            
            if int(outfit_type) == 1:
                upload_images = request.FILES.getlist("outfit_images")
                
                for image in upload_images:
                    if image:
                        OutfitImage.objects.create(
                            outfit=outfit,
                            outfit_image=image
                        )
                        
                urls = request.POST.getlist("outfit_urls")
                for url in urls:
                    if url.strip():
                        OutfitUrl.objects.create(
                            outfit=outfit,
                            url=url.strip()
                        )
            
            if int(outfit_type) == 0:
                selected_ids = request.POST.getlist("selected_clothing_item_ids")
                
                if owner_type == "user":
                    available_items = ClothingItem.objects.filter(user=owner)
                else:
                    available_items = ClothingItem.objects.filter(child=owner)
                
                for clothing_item_id in selected_ids:
                    if clothing_item_id:
                        clothing_item = get_object_or_404(available_items, pk=clothing_item_id)
                        OutfitClothingItem.objects.create(
                            outfit=outfit,
                            clothing_item=clothing_item
                        )
            
            if owner_type == "user":
                if outfit.is_favorite:
                    return redirect("user_favorite_outfit_list", owner_id=owner.pk)
                return redirect("user_outfit_list", owner_id=owner.pk)
            else:
                if outfit.is_favorite:
                    return redirect("child_favorite_outfit_list", owner_id=owner.pk)
                return redirect("child_outfit_list", owner_id=owner.pk)
            
    else:
        initial_data = {}
        
        if int(outfit_type) == 1:
            initial_data["is_favorite"] = True
            
        form = OutfitForm(initial=initial_data)
        
    if int(outfit_type) == 0:
        initial_slot_count = 3
        clothing_items = ClothingItem.objects.filter(user=owner) if owner_type == "user" else ClothingItem.objects.filter(child=owner)
        categories = Category.objects.all()
        color_choices = ClothingItem.COLOR_CHOICES
    else:
        initial_slot_count = 2
        clothing_items = []
        categories = []
        color_choices = []
        
    context = {
        "form": form,
        "owner": owner,
        "owner_type": owner_type,
        "outfit_type": int(outfit_type),
        "initial_slot_count": initial_slot_count,
        "initial_slots": range(initial_slot_count),
        "clothing_items": clothing_items,
        "categories": categories,
        "color_choices": color_choices,
        "selected_category": "",
        "selected_color": "",
        "is_create": True,
    }
    
    return render(request, "cordinate/outfit_form.html", context)

@login_required
def clothing_item_search_create(request, owner_type, owner_id):
    if owner_type == "user":
        owner = get_object_or_404(User, pk=owner_id)
        if owner.family != request.user.family:
            return redirect("home")
        clothing_items = ClothingItem.objects.filter(user=owner)
    else:
        owner = get_object_or_404(Child, pk=owner_id)
        if owner.family != request.user.family:
            return redirect ("home")
        clothing_items = ClothingItem.objects.filter(child=owner)
        
    category_id = request.GET.get("category")
    color = request.GET.get("color")
    
    if category_id:
        clothing_items = clothing_items.filter(category_id=category_id)
        
    if color:
        clothing_items = clothing_items.filter(color=color)
        
    context = {
        "clothing_items": clothing_items,
    }
    
    return render(request, "cordinate/_clothing_item_search_results.html", context)
    

@login_required
def outfit_detail(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    
    if outfit.user:
        if outfit.user.family != request.user.family:
            return redirect("home")
        owner = outfit.user
        owner_type = "user"
    else:
        if outfit.child.family != request.user.family:
            return redirect("home")
        owner = outfit.child
        owner_type = "child"
        
    next_url =request.GET.get("next", "")
    
    context = {
        "outfit": outfit,
        "owner": owner,
        "owner_type": owner_type,
        "next_url": next_url,
    }
    
    return render(request, "cordinate/outfit_detail.html", context)

@login_required
def outfit_update(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    
    if outfit.user:
        if outfit.user.family != request.user.family:
            return redirect("home")
        owner = outfit.user
        owner_type = "user"
    else:
        if outfit.child.family != request.user.family:
            return redirect("home")
        owner = outfit.child
        owner_type = "child"
    
    if request.method == "POST":
        form = OutfitForm(request.POST, instance=outfit)
        
        if form.is_valid():
            outfit = form.save()
            
            #外部サイトコーデ画像登録
            if outfit.outfit_type == 1:
                keep_image_ids = request.POST.getlist("keep_outfit_image_ids")
                
                outfit.outfit_images.exclude(pk__in=keep_image_ids).delete()
                
                upload_images = request.FILES.getlist("outfit_images")
                
                for image in upload_images:
                    if image:
                        OutfitImage.objects.create(
                            outfit=outfit,
                            outfit_image=image
                        )
            
                #外部サイトコーデURL保存
                outfit.outfit_urls.all().delete()
                
                urls = request.POST.getlist("outfit_urls")
                for url in urls:
                    if url.strip():
                        OutfitUrl.objects.create(
                            outfit=outfit,
                            url=url.strip()
                        )
            
            
            #手持ちコーデ画像登録
            if outfit.outfit_type == 0:
                selected_ids = request.POST.getlist("selected_clothing_item_ids")
                
                outfit.outfit_clothing_items.all().delete()
                
                if outfit.user:
                    available_items = ClothingItem.objects.filter(user=outfit.user)
                else:
                    available_items = ClothingItem.objects.filter(child=outfit.child)
                    
                for clothing_item_id in selected_ids:
                    if clothing_item_id:
                        clothing_item = get_object_or_404(available_items, pk=clothing_item_id)
                        OutfitClothingItem.objects.create(
                            outfit=outfit,
                            clothing_item=clothing_item
                        )
            
            is_favorite = outfit.is_favorite
              
            if owner_type == "user":
                if is_favorite:
                    return redirect("user_favorite_outfit_list", owner_id=owner.pk)
                return redirect("user_outfit_list", owner_id=owner.pk)
            else:
                if is_favorite:
                    return redirect("child_favorite_outfit_list", owner_id=owner.pk)
                return redirect("child_outfit_list", owner_id=owner.pk)
    else:
        form = OutfitForm(instance=outfit)
        
    if outfit.outfit_type == 0:
        if outfit.user:
            clothing_items = ClothingItem.objects.filter(user=outfit.user).exclude(
                id__in=outfit.outfit_clothing_items.values_list("clothing_item_id", flat=True)
            )
        else:
            clothing_items = ClothingItem.objects.filter(child=outfit.child).exclude(
                id__in=outfit.outfit_clothing_items.values_list("clothing_item_id", flat=True)
            )
        
        categories = Category.objects.all()
        color_choices = ClothingItem.COLOR_CHOICES
        
    else:
        clothing_items = []
        categories = []
        color_choices = []
        
    
    context = {
        "form": form,
        "outfit": outfit,
        "owner": owner,
        "owner_type": owner_type,
        "outfit_type": outfit.outfit_type,
        "is_create": False,
        "clothing_items": clothing_items,
        "categories": categories,
        "color_choices": color_choices,
        "selected_category": "",
        "selected_color": "",
    }
    
    return render(request, "cordinate/outfit_form.html", context)

@login_required
def clothing_item_search(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    
    if outfit.user:
        if outfit.user.family != request.user.family:
            return redirect("home")
        clothing_items = ClothingItem.objects.filter(user=outfit.user)
    else:
        if outfit.child.family != request.user.family:
            return redirect("home")
        clothing_items = ClothingItem.objects.filter(child=outfit.child)
        
    category_id = request.GET.get("category")
    color = request.GET.get("color")
    
    if category_id:
        clothing_items = clothing_items.filter(category_id=category_id)
        
    if color:
        clothing_items = clothing_items.filter(color=color)
        
    current_item_ids = outfit.outfit_clothing_items.values_list("clothing_item_id", flat=True)
    clothing_items = clothing_items.exclude(id__in=current_item_ids)
    
    categories = Category.objects.all()
    color_choices = ClothingItem.COLOR_CHOICES
    
    context = {
        "outfit": outfit,
        "clothing_items": clothing_items,
        "categories": categories,
        "color_choices": color_choices,
        "selected_category": category_id,
        "selected_color": color,
    }
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "cordinate/_clothing_item_search_results.html", context)
    
    return render(request, "cordinate/_clothing_item_search_results.html", context)

@login_required
def outfit_delete(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    
    if outfit.user:
        if outfit.user.family != request.user.family:
            return redirect("home")
        owner = outfit.user
        owner_type = "user"
    else:
        if outfit.child.family != request.user.family:
            return redirect("home")
        owner = outfit.child
        owner_type = "child"
    
    if request.method == "POST":
        next_url = request.POST.get("next", "")
        outfit.delete()
        
        if owner_type == "user":
            return redirect("user_outfit_list", owner_id=owner.pk)
        else:
            return redirect("child_outfit_list", owner_id=owner.pk)
    
    return redirect("outfit_detail", pk=outfit.pk)

@login_required
def favorite_outfit_list(request, owner_type, owner_id):
    if owner_type == "user":
        owner = get_object_or_404(
            User,
            pk=owner_id,
            family=request.user.family
        )
        outfits = Outfit.objects.filter(user=owner, is_favorite=True)
    else:
        owner = get_object_or_404(
            Child,
            pk=owner_id,
            family=request.user.family
        )
        outfits = Outfit.objects.filter(child=owner, is_favorite=True)
        
    order = request.GET.get("order", "new")
    
    if order == "old":
        outfits = outfits.order_by("created_at")
    else:
        outfits = outfits.order_by("-created_at")
        
    context = {
        "owner": owner,
        "owner_type": owner_type,
        "outfits": outfits,
        "order": order,
    }
    
    return render(request, "cordinate/favorite_outfit_list.html", context)

@login_required
def outfit_image_delete(request, pk):
    outfit_image = get_object_or_404(OutfitImage, pk=pk)
    outfit = outfit_image.outfit
    
    if outfit.user:
        if outfit.user.family != request.user.family:
            return redirect("home")
        owner = outfit.user
        owner_type = "user"
    else:
        if outfit.child.family != request.user.family:
            return redirect("home")
        owner = outfit.child
        owner_type = "child"
        
    if request.method == "POST":
        outfit_image.delete()
        
        return redirect("outfit_update", pk=outfit.pk)
    
    return redirect("outfit_update", pk=outfit.pk)

def outfit_select(request, owner_type, owner_id):
    if owner_type == "user":
        owner = get_object_or_404(User, pk=owner_id)
        if owner.family != request.user.family:
            return redirect("home")
    else:
        owner = get_object_or_404(Child, pk=owner_id)
        if owner.family != request.user.family:
            return redirect("home")
        
    context = {
        "owner": owner,
        "owner_type": owner_type,
    }
            
    return render(request, "cordinate/outfit_select.html", context)

def nursery_item_create(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    
    if child.family != request.user.family:
        return redirect("home")
    
    if request.method == "POST":
        form = NurseryItemForm(request.POST)
        if form.is_valid():
            nursery_item = form.save(commit=False)
            nursery_item.child = child
            nursery_item.save()
            return redirect("nursery_item_list", child_id=child.pk)
    else:
        form = NurseryItemForm()
    
    context = {
        "child": child,
        "form": form,
    }
    return render(request, "cordinate/nursery_item_form.html", context)

def nursery_item_list(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    
    if child.family != request.user.family:
        return redirect("home")
    
    carry_items = NurseryItem.objects.filter(
        child=child,
        item_type=0
    ).order_by("created_at")
    
    stock_items = NurseryItem.objects.filter(
        child=child,
        item_type=1
    ).order_by("created_at")
    
    context = {
        "child": child,
        "carry_items": carry_items,
        "stock_items": stock_items,
    }
    
    return render (request, "cordinate/nursery_item_list.html", context)

def nursery_item_check(request, item_id):
    item = get_object_or_404(NurseryItem, pk=item_id)
    
    if item.child.family != request.user.family:
        return redirect("home")
    
    if request.method == "POST":
        item.is_checked = True
        item.save()
        
    return redirect("nursery_item_list", child_id=item.child.pk)
    
     