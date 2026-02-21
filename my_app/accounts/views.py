from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model,login
from .forms import SignUpForm
from .models import Family


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
    

        
