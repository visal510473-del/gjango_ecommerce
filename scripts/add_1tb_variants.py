import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product, ProductVariant

TARGET_KEYWORDS = ['17 pro max', '17 pro', '17 air', '16 pro max', '16 pro']
COLORS = ['Black', 'White', 'Silver', 'Orange', 'Blue']
STORAGE = '1TB'

def main():
    total = 0
    for kw in TARGET_KEYWORDS:
        qs = Product.objects.filter(name__icontains=kw)
        for p in qs:
            for color in COLORS:
                obj, created = ProductVariant.objects.get_or_create(product=p, color=color, storage=STORAGE)
                if created:
                    print(f'Created 1TB variant for product id={p.id} name="{p.name}" color={color}')
                    total += 1
    print('Done. Created total:', total)

if __name__ == '__main__':
    main()
