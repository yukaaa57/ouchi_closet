from django import forms
from .models import ClothingItem, Category, Season, SIZE_CHOICES

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
            "clothing_image",
            "category",
            "size",
            "color",
            "seasons",
            "wear_status",
            "note",
        ]
        labels = {
             "clothing_image":"画像",
            "category":"カテゴリ",
            "size":"サイズ",
            "color":"カラー",
            "wear_status":"着用状況",
            "note":"メモ",
        }
        widget = {
            "category": forms.Select(),
            "size": forms.Select(),
            "color": forms.Select(),
            "wear_status": forms.Select(),
            "note": forms.Textarea(attrs={"rows": 4}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {"name": "カテゴリ名"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "カテゴリ名"}),
        }

class ClothingSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="カテゴリ",
        empty_label="選択して下さい",
    )
    
    size = forms.ChoiceField(
        choices=[("", "選択して下さい")]+ list(SIZE_CHOICES),
        required=False,
        label="サイズ",
    )
    
    color = forms.ChoiceField(
        choices=[("", "選択して下さい")]+ list(ClothingItem.COLOR_CHOICES),
        required=False,
        label="カラー",
    )
    
    season = forms.ModelMultipleChoiceField(
        queryset=Season.objects.all(),
        required=False,
        label="季節",
        widget=forms.CheckboxSelectMultiple,
    )
    
    wear_status = forms.ChoiceField(
        choices=[("", "選択して下さい")]+ list(ClothingItem.WEAR_STATUS_CHOICES),
        required=False,
        label="着用状況",
    )