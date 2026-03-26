from django import forms
from .models import Outfit

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ["note", "external_url"]
        labels = {
            "note": "メモ",
            "external_url": "外部サイトURL",
        }
        