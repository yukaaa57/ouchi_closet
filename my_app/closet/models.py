from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Child, SIZE_CHOICES, Family

User = get_user_model()

class Category(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name 

class ClothingItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothes",
    )
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothes",
    )
    
    clothing_image = models.ImageField(upload_to="clothing_photos/")
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="clothes",
    )
    
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    
    COLOR_CHOICES =(
        ("white", "白"),
        ("black", "黒"),
        ("navy", "紺"),
        ("brown", "茶"),
        ("beige", "ベージュ"),
        ("gray", "グレー"),
        ("khaki", "カーキ"),
        ("green", "緑"),
        ("blue", "青"),
        ("red", "赤"),
        ("pink", "ピンク"),
        ("purple", "紫"),
        ("yellow", "黄"),
        ("orange", "オレンジ"),
        ("other", "その他"),
    )
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    
    seasons = models.ManyToManyField(Season, related_name="clothes")
    
    WEAR_STATUS_CHOICES =(
        ("unused", "未使用"),
        ("justsize", "ジャストサイズ"),
        ("large", "大きめ"),
        ("small", "小さめ"),
        ("rarely", "あまり着ていない"),
        ("sizeout", "サイズアウト"),
    )
    wear_status =models.CharField(max_length=20, choices=WEAR_STATUS_CHOICES, blank=True)
    
    note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            owner_name = self.user.nickname
        elif self.child:
            owner_name = self.child.nickname
        else:
            owner_name = "未設定"
        
        return f"{owner_name} / {self.category.name}"
    
    