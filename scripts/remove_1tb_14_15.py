import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django

django.setup()

from products.models import Product, ProductVariant

KEYWORDS = ['iphone 15', 'iphone 14']
removed = 0
for kw in KEYWORDS:
    for p in Product.objects.filter(name__icontains=kw):
        qs = p.variants.filter(storage__iexact='1TB')
        count = qs.count()
        if count:
            print(f'Removing {count} 1TB variants from product id={p.id} name="{p.name}"')
            removed += count
            qs.delete()
print('Done. Removed total 1TB variants:', removed)
