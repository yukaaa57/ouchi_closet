from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    from_class = SignUpForm
    template_name = "registration/signup.html"
    succes_url = reverse_lazy("login")
    
# Create your views here.
