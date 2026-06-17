import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product, ProductVariant

def main():
    name = 'iphone 17 pro max'
    try:
        product = Product.objects.get(name__iexact=name)
    except Product.DoesNotExist:
        qs = Product.objects.filter(name__icontains='iphone')
        if qs.exists():
            product = qs.first()
            print(f"Using product found by contains: {product.name} (id={product.id})")
        else:
            print('Product not found by name or contains.')
            return

    variants_to_create = [
        ('Orange', '256GB'),
        ('Black', '512GB'),
        ('Silver', '128GB'),
    ]

    for color, storage in variants_to_create:
        v, created = ProductVariant.objects.get_or_create(product=product, color=color, storage=storage)
        print(('Created' if created else 'Exists') + f' variant id={v.id} {color} {storage}')

    print('Done. Product id:', product.id, 'variants count:', product.variants.count())

if __name__ == '__main__':
    main()
