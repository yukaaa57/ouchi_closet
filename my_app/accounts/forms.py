from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("profile_image", "nickname", "size", "email")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("profile_image", "nickname", "size", "email")
        