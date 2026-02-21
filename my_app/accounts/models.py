from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
import uuid
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("メールは必須です")
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
def create_superuser(self, email, password=None):
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

SIZE_CHOICES = [
    ("","未設定"),
    ("70","70"),
    ("80","80"),
    ("90","90"),
    ("95","95"),
    ("100","100"),
    ("110","110"),
    ("120","120"),
    ("130","130"),
    ("140","140"),
    ("150","150"),
    ("S","S"),
    ("M","M"),
    ("L","L"),
    ("LL","LL"),
    ("XL","XL"),
    ("その他","その他"),   
]

class Family(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Family {self.id}"

class User(AbstractBaseUser, PermissionsMixin):
    profile_image = models.ImageField(
        verbose_name="プロフィール画像",
        upload_to="profile_images",
        null=True,
        blank=True,
    )
    nickname = models.CharField(
        verbose_name="ニックネーム",
        max_length=100,
    )
    size = models.CharField(
        verbose_name="サイズ",
        max_length=10,
        choices=SIZE_CHOICES,
        blank=True,
        default="",
    )
    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    objects = UserManager()
   
    USERNAME_FIELD = 'email' 
    
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
