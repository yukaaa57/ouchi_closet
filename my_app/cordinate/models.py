from django.db import models
from accounts.models import User, Child
from closet.models import ClothingItem

class Outfits(models.Model):
    OUTFIT_TYPE_CHOICES = (
        (0, "internal"),
        (1, "external"),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="ユーザー"
    )
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="子ども"
    )
    
    outfit_type = models.IntegerField(
        choices=OUTFIT_TYPE_CHOICES,
        verbose_name="コーデ種別"
    )
    
    note = models.TextField(
        blank=True,
        verbose_name="メモ"
    )
    
    is_favorite = models.BooleanField(
        default=False,
        verbose_name="お気に入り"
    )
    
    external_url = models.URLField(
        blank=True,
        verbose_name="外部サイトURL"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            owner_name = self.user.nickname
        elif self.child:
            owner_name = self.child.nickname
        else:
            owner_name = "未設定"
        
        return f"{owner_name}のコーデ{self.id}"
    

            
        