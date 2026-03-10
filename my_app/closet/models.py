from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Child, SIZE_CHOICES

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name 
