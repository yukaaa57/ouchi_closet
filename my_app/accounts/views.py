from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login
from .forms import SignUpForm
from .models import Family, Invitation


User = get_user_model()

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    
    def form_valid(self, form):
        user = form.save()
        family = Family.objects.create()
        user.family = family
        user.save
        login(self.request, user)
        return redirect("/")
    
    success_url = reverse_lazy("/")

@login_required
def invite_view(request):
    family = request.user.family

    #familyのないユーザーは招待リンク出せない
    if family is None:
        return render(request, "registration/invite.html", {"error":"家族が未設定です"})
    
    #未使用の招待を新しい順に探す
    invites = family.invitations.order_by("-created_at")
    
    invite = None
    for i in invites:
        #is_valid()の中で期限切れならstatus=EXPIREDに更新
        if i.is_valid():
            invite = i
            break
    
    #有効なものがなければ新規作成
    if invite is None:
        invite = Invitation.objects.create(
            family=family,
            created_by=request.user,
            token=Invitation.generate_token(),
        )
    
    invite_url = request.build_absolute_uri(f"/accounts/signup/?invite={invite.token}")
    return render(request, "registration/invite.html", {"invite_url": invite_url})


        
