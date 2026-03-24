from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User, Child
from .models import Outfit

@login_required
def outfit_list(request, owner_type, oewner_id):
    if owner_type == "user":
        owner = get_object_or_404(
            User,
            pk=oewner_id,
            family=request.user.family
        )
        outfits = Outfit.objects.filter(user=owner).order_by("-created_at")
    else:
        owner = get_object_or_404(
            Child,
            pk=oewner_id,
            family=request.user.family
        )
        outfits = Outfit.objects.filter(child=owner).order_by("-created_at")
    
    context = {
        "owner": owner,
        "owner_type": owner_type,
        "outfits": outfits,
    }
    
    return render(request, "cordinate/outfit_list.html", context)
