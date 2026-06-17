import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product, ProductVariant

def main():
    created = 0
    for p in Product.objects.all():
        if p.variants.count() == 0:
            v = ProductVariant.objects.create(product=p, color='Default', storage='128GB')
            print(f'Created variant for product id={p.id} name="{p.name}" -> variant id={v.id}')
            created += 1
    print('Done. Variants created:', created)

if __name__ == '__main__':
    main()
