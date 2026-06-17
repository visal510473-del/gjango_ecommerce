import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_mobix.settings')
import django
django.setup()

from products.models import Product

for pid in [17, 18, 19, 20, 21, 22]:
    p = Product.objects.get(id=pid)
    print('---', pid, p.name)
    for v in p.variants.all().order_by('storage', 'color'):
        print(v.id, repr(v.color), repr(v.storage))
