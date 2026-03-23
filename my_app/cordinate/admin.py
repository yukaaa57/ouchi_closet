from django.contrib import admin
from .models import Outfit, OutfitClothingItem, OutfitImage

class OutfitClothingItemInline(admin.TabularInline):
    model = OutfitClothingItem
    extra = 1
    
class OutfitImageInline(admin.TabularInline):
    model = OutfitImage
    extra = 1
    
@admin.register(Outfit)
class OutfirAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "child", "outfit_type", "is_favorite", "created_at")
    inlines = [OutfitClothingItemInline, OutfitImageInline]    
    
@admin.register(OutfitClothingItem)
class OutfitlothingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "outfit", "clothing_item")
    
@admin.register(OutfitImage)
class OutfitImageAdmin(admin.ModelAdmin):
    list_display = ("id", "outfit", "outfit_image")