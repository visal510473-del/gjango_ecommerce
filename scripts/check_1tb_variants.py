import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product

def main():
    print('Product ID | Name | total_variants | 1TB_variants')
    for p in Product.objects.all().order_by('id'):
        total = p.variants.count()
        tb = p.variants.filter(storage__iexact='1TB').count()
        print(f'{p.id:9} | {p.name} | {total:14} | {tb}')

if __name__ == '__main__':
    main()
