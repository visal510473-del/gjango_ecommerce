import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product, ProductVariant

DEFAULT_COLORS = ['Black', 'White', 'Silver', 'Orange', 'Blue']
STORAGE = '1TB'

def main():
    created_total = 0
    for p in Product.objects.all().order_by('id'):
        tb_count = p.variants.filter(storage__iexact=STORAGE).count()
        if tb_count > 0:
            continue

        colors = list(p.variants.values_list('color', flat=True).distinct())
        if not colors:
            colors = DEFAULT_COLORS

        for color in colors:
            obj, created = ProductVariant.objects.get_or_create(product=p, color=color, storage=STORAGE)
            if created:
                print(f'Created 1TB variant for product id={p.id} name="{p.name}" color={color}')
                created_total += 1

    print('Done. Created total 1TB variants:', created_total)

if __name__ == '__main__':
    main()
