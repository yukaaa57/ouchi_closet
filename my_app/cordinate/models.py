from django.db import models
from accounts.models import User, Child
from closet.models import ClothingItem

class Outfit(models.Model):
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
    
class OutfitClothingItem(models.Model):
    outfit = models.ForeignKey(
        Outfit,
        on_delete=models.CASCADE,
        related_name="outfit_clothing_items",
        verbose_name="コーディネート"
    )
    
    clothing_item = models.ForeignKey(
        ClothingItem,
        on_delete=models.CASCADE,
        verbose_name="洋服アイテム"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.outfit} - {self.clothing_item}"
    
class OutfitImage(models.Model):
    outfit = models.ForeignKey(
        Outfit,
        on_delete=models.CASCADE,
        related_name="outfit_images",
        verbose_name="コーディネート"
    )
    
    outfit_image = models.ImageField(
        upload_to="cordinate/",
        verbose_name="コーデ画像"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.outfit}の画像"
    
class OutfitUrl(models.Model):
    outfit = models.ForeignKey(
        "Outfit",
        on_delete=models.CASCADE,
        related_name="outfit_urls"
    )
    url = models.URLField()
    
    def __str__(self):
        return self.url
    
class NurseryItem(models.Model):
    ITEM_TYPE_CHOICES = (
        (0, "持ち物"),
        (1, "必要な物"),
    )
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name="nursery_items"
    )
    item_type = models.ImageField(choices=ITEM_TYPE_CHOICES)
    name = models.CharField(max_length=50)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
            
        