from django.contrib import admin
from .models import Product, ProductVariant, CartItem # នាំចូល Model ទាំងអស់ដែលប្អូនមាន

# ចុះឈ្មោះ Model ឱ្យវាបង្ហាញក្នុង Admin Panel
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(CartItem)