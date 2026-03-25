from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from .models import Outfit

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