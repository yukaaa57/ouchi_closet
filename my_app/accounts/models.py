from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
import uuid
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets

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
    family = models.ForeignKey(
        Family,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
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
    
class Invitation(models.Model):
    STATUS_UNUSED = 0
    STATUS_USED = 1
    STATUS_EXPIRED = 2
    
    STATUS_CHOICES =(
        (STATUS_UNUSED, "未使用"),
        (STATUS_USED, "使用済み"),
        (STATUS_EXPIRED, "失効"),
    )
    family = models.ForeignKey("accounts.Family", on_delete=models.CASCADE, related_name="invitations")
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="issued_invitations")
    token = models.CharField(max_length=32, unique=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_UNUSED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    
    #token生成
    @classmethod
    def generate_token(cls):
        return secrets.token_hex(16)
    
    #デフォルトの有効期限（24時間）
    @classmethod
    def default_expires_at(cls):
        return timezone.now() + timedelta(hours=24)
    
    #使用済みにする
    def mark_used(self):
        self.status = self.STATUS_USED
        self.used_at = timezone.now()
        self.save()
        
    #失効処理
    def mark_expired(self):
        self.status = self.STATUS_EXPIRED
        self.save()
        
    #有効判定（＋期限切れなら自動でEXPIREDに変更）
    def is_valid(self):
        if self.status == self.STATUS_USED:
            return False
        if self.status == self.STATUS_EXPIRED:
            return False
        if timezone.now() >= self.expires_at:
            return False
        return True
    
    #expires_atが未設定なら自動設定
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.default_expires_at()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Invite({self.token}) starus={self.status}"
    
                
    
    