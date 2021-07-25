from mainapp.models import ProductCategory


categories = [
    "HOME",
    "OFFICE",
    "FURNITURE",
    "MODERN",
    "CLASSIC",
    "LIGHTING",
    "CHAIRS",
    "SOFAS",
]


for category in categories:
    added_category = ProductCategory(name=category)
    added_category.save()


