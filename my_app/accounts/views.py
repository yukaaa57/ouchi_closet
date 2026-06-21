from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import SignUpForm, ProfileUpdateForm, ChildCreateForm, ChildForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm, LoginForm
from .models import User, Family, Invitation, Child
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, LoginView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from closet.utils import create_default_categories
from django.db import transaction

User = get_user_model()

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invite = self.request.GET.get("invite")
        context["invite"] = invite
        return context
    
    def form_valid(self, form):
       
        invite_token = (self.request.POST.get("invite") or "").strip()
        invitation = None
        
        with transaction.atomic():
            user = form.save(commit=False)
            if invite_token:
                try:
                    invitation = Invitation.objects.get(token=invite_token)
                    
                    if not invitation.is_valid():
                        form.add_error(None, "招待リンクが無効または期限切れです")
                        return self.form_invalid(form)
                    
                    user.family = invitation.family
                    
                except Invitation.DoesNotExist:
                    form.add_error(None, "無効な招待リンクです")
                    return self.form_invalid(form)
                
            else:
                family = Family.objects.create()
                create_default_categories(family)
                user.family = family
            user.save()
            
            login(self.request, user)
            
            if invitation is not None:
                invitation.mark_used()
        
        messages.success(self.request, "登録しました。")
        return redirect(self.success_url)
        
class CustomLoginView(LoginView):
    form_class = LoginForm
        
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

@login_required
def home(request):
    family = request.user.family
    
    family_users = User.objects.filter(family=family)
    children = Child.objects.filter(family=family)
    
    return render(request, "home.html", {
        "family_users": family_users,
        "children": children,
    })

@login_required
def user_closet(request, pk):
    user = get_object_or_404(User, pk=pk, family=request.user.family)
    return HttpResponse(f"{user.nickname}のクローゼット（仮）")

@login_required
def child_closet(request, pk):
    child = get_object_or_404(Child, pk=pk, family=request.user.family)
    return HttpResponse(f"{child.nickname}のクローゼット（仮）")

@login_required
def me_view(request):
    return render(request, "accounts/me.html", {"user_obj":request.user})

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    form_class = ProfileUpdateForm
    template_name = "accounts/me_edit.html"
    success_url = reverse_lazy("me")
    
    def get_object(self, queryset = None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "アカウント情報を変更しました。")
        return super().form_valid(form)
    
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("me")
    
    def form_valid(self, form):
        messages.success(self.request, "パスワードを変更しました。")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = "registration/password_reset_confirm.html"
    
class ChildCreateView(LoginRequiredMixin, CreateView):
    model = Child
    form_class = ChildCreateForm
    template_name = "accounts/child_form.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        child = form.save(commit=False)
        child.family = self.request.user.family
        child.save()
        
        messages.success(self.request, "お子さまを追加しました。")
        return super().form_valid(form)
    
class ChildUpdateView(LoginRequiredMixin, UpdateView):
    model = Child
    form_class = ChildForm
    template_name = "accounts/child_edit.html"
    success_url = reverse_lazy("home")
    
    def get_queryset(self):
        return Child.objects.filter(family=self.request.user.family)
    
    def form_valid(self, form):
        messages.success(self.request, "お子さま情報を変更しました。")
        return super().form_valid(form)

def user_closet(request, pk):
    user = get_object_or_404(User, pk=pk, family=request.user.family)
    return HttpResponse(f"{user.nickname}のクローゼット")

def child_closet(request, pk):
    child = get_object_or_404(Child, pk=pk, family=request.user.family)
    return HttpResponse(f"{child.nickname}のクローゼット")
    
def portfolio(request):
    return render(request, "portfolio.html")
    
    
    
    


        
