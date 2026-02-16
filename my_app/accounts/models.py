from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)

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

class User(AbstractBaseUser, PermissionsMixin):
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
    
