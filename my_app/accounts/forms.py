import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from .models import User, Child
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

def validate_custom_password(password, user=None):
    errors = []
    
    if len(password) < 8:
        errors.append("パスワードは最低８文字以上で入力してください。")
    
    has_letter = re.search(r"[A-Za-z]", password)
    has_number = re.search(r"\d", password)
    has_symbol = re.search(r"[!-/:-@[-`{-~]", password)
    
    if not (has_letter and has_number and has_symbol):
        errors.append("パスワードは英字・数字・記号を含めてください。")
        
    user_infos = [
        getattr(user, "email", ""),
        getattr(user, "username", ""),
        getattr(user, "nickname", ""),
    ]
    
    for info in user_infos:
        if info and info.lower() in password.lower():
            errors.append("個人情報と似ているパスワードは使用できません。")
            break
    
    return errors

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("profile_image", "nickname", "size", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["password1"].help_text = """
        <ul>
            <li>個人情報と似たパスワードは使用できません</li>
            <li>８文字以上で入力してください</li>
            <li>英字・数字・記号を含めてください</li>
        </ul>
        """
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        errors = []
        
        if password1:
            if len(password1) < 8:
                errors.append("パスワードは最低８文字以上で入力してください。")
                
            has_letter = re.search(r"[A-Za-z]", password1)
            has_number = re.search(r"\d", password1)
            has_symbol = re.search(r"[!-/:-@[-`{-~]", password1)
            
            if not (has_letter and has_number and has_symbol):
                errors.append("パスワードは英字・数字・記号を含めてください。")
                
        if password1 and password2 and password1 != password2:
            errors.append("確認用パスワードが一致しません。")
            
        for error in errors:
            self.add_error("password1", error)
            
        return cleaned_data
        

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

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        
        self.fields["new_password1"].help_text = """
        <ul>
            <li>個人情報と似たパスワードは使用できません</li>
            <li>８文字以上で入力してください</li>
            <li>英字・数字・記号を含めてください</li>
        </ul>
        """
    
    def clean_new_password2(self):
        return self.cleaned_data.get("new_password2")
    
    def clean(self):
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        
        errors = []
        
        if password1:
            errors += validate_custom_password(password1, self.user)
        
        if password1 and password2 and password1 != password2:
            errors.append("確認用パスワードが一致しません。")
            
        for error in errors:
            self.add_error("new_password1", error)
        
        return cleaned_data
    
class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        
        self.fields["new_password1"].help_text = """
        <ul>
            <li>個人情報と似たパスワードは使用できません</li>
            <li>８文字以上で入力してください</li>
            <li>英字・数字・記号を含めてください</li>
        </ul>
        """
    
    def clean_new_password2(self):
        return self.cleaned_data.get(self.new_password2)
    
    def clean(self):
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        
        errors = []
        
        if password1:
            self.errors += validate_custom_password(password1, self.user)
            
        if password1 and password2 and password1 != password2:
            self.errors.append("確認用パスワードが一致しません。")
            
        for error in errors:
            self.add_error("new_password1", error)
            
        return cleaned_data
