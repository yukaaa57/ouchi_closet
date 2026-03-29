from django import forms
from .models import Outfit, OutfitImage, OutfitClothingItem

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ["is_favorite", "note", "external_url"]
        labels = {
            "is_favorite": "お気に入り",
            "note": "メモ",
            "external_url": "外部サイトURL",
        }
        
class OutfitImageForm(forms.ModelForm):
    class Meta:
        model = OutfitImage
        fields = ["outfit_image"]
        labels = {"outfit_image": "画像"}
    
        