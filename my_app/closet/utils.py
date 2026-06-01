from .models import Category

DEFAULT_CATEGORIES = [
    "トップス",
    "ボトムス",
    "ワンピース",
    "アウター",
    "セットアップ",
    "シューズ",
    "小物",
    "バッグ",
]

def create_default_categories(family):
    for index, name in enumerate(DEFAULT_CATEGORIES):
        Category.objects.get_or_create(
            family=family,
            name=name,
            defaults={
                "sort_order": index,
                "is_default": True,
            }
        )