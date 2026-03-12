from django.contrib import admin
from .models import Category, Season, ClothingItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")

@admin.register(Season)
class SeasinAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    
@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "child", "category", "size", "color", "seasons", "wear_status", "created_at")
    
    

