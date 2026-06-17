import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product, ProductVariant

COLORS = ['Black', 'White', 'Silver', 'Orange', 'Blue']
STORAGES = ['128GB', '256GB', '512GB']

def main():
    created_total = 0
    for p in Product.objects.all():
        created_for_p = 0
        for color in COLORS:
            for storage in STORAGES:
                obj, created = ProductVariant.objects.get_or_create(
                    product=p,
                    color=color,
                    storage=storage,
                )
                if created:
                    created_for_p += 1
                    created_total += 1
        if created_for_p:
            print(f'Product id={p.id} "{p.name}": created {created_for_p} variants')
    print('Done. Total variants created:', created_total)

if __name__ == '__main__':
    main()
