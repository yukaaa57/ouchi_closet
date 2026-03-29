from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from .models import Outfit, OutfitImage
from .forms import OutfitForm, OutfitImageForm

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
            form.save()
            
            if outfit.outfit_type == 1:
                upload_images = request.FILES.getlist("outfit_images")
                
                for image in upload_images:
                    if image:
                        OutfitImage.objects.create(
                            outfit=outfit,
                            outfit_image=image
                        )
            
            is_external = outfit.outfit_type == 1
            is_favorite = outfit.is_favorite
              
            if owner_type == "user":
                if is_external or is_favorite:
                    return redirect("user_favorite_outfit_list", owner_id=owner.pk)
                return redirect("user_outfit_list", owner_id=owner.pk)
            else:
                if is_external or is_favorite:
                    return redirect("child_favorite_outfit_list", owner_id=owner.pk)
                return redirect("child_outfit_list", owner_id=owner.pk)
    else:
        form = OutfitForm(instance=outfit)
    
    context = {
        "form": form,
        "outfit": outfit,
        "owner": owner,
        "owner_type": owner_type,
    }
    
    return render(request, "cordinate/outfit_form.html", context)

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
        outfit.delete()
        
        if owner_type == "user":
            return redirect("user_outfit_list", owner_id=owner.pk)
        else:
            return redirect("child_outfit_list", owner_id=owner.pk)
    
    return redirect("outfit_deteil", pk=outfit.pk)

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
        
        return redirect("outfit_uodate", pk=outfit.pk)
    
    return redirect("outfit_uodate", pk=outfit.pk)
     