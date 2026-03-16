from django import forms
from .models import ClothingItem, Category, Season

class ClothingItemForm(forms.ModelForm):
    seasons = forms.ModelMultipleChoiceField(
        queryset=Season.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="季節",
    )
    
    class Meta:
        model = ClothingItem
        fields = [
            "photo",
            "category",
            "size",
            "color",
            "seasons",
            "wear_status",
            "memo",
        ]
        labels = {
             "photo":"画像",
            "category":"カテゴリ",
            "size":"サイズ",
            "color":"カラー",
            "wear_status":"着用状況",
            "memo":"メモ",
        }
        widget = {
            "category": forms.Select(),
            "size": forms.Select(),
            "color": forms.Select(),
            "wear_status": forms.Select(),
            "memo": forms.Textarea(attrs={"rows": 4}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {"name": "カテゴリ名"}
        wodgets = {
            "name": forms.TextInput(attrs={"placeholder": "カテゴリ追加"})
        }