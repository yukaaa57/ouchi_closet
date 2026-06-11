from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User, Child
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("profile_image", "nickname", "size", "email", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1:
            try:
                validate_password(password1, self.instance)
            except ValidationError as e:
                for message in e.messages:
                    self.add_error("password1", message)
                    
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "確認用パスワードが一致しません。")
            
        return self.cleaned_data
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("profile_image", "nickname", "size", "email")
        
class ChildCreateForm(forms.ModelForm):
    class Meta:
        model = Child
        fields =  ("profile_image", "nickname", "size", "birthday")
        
        #生年月日をカレンダーに
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}),
        }
        
class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ("profile_image", "nickname", "size", "birthday")
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}),
        }