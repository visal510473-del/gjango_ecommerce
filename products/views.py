from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductVariant, CartItem

def home(request):
    # ប្រើ prefetch_related ដើម្បីឱ្យទំព័រ home ដើរលឿនជាងមុន
    products = Product.objects.prefetch_related('variants').all()
    return render(request, 'products/home.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.all()
    similar_products = Product.objects.exclude(pk=pk).order_by('?')[:4]
    return render(request, 'products/detail.html', {
        'product': product,
        'variants': variants,
        'similar_products': similar_products,
    })

@login_required 
def add_to_cart(request, product_id):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        
        # រកមើល variant តាម id
        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        # បញ្ចូលក្នុង Cart ឬបូកចំនួនបន្ថែម
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, 
            variant=variant
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
        return redirect('cart_view') # ត្រូវប្រាកដថាមាន name='cart_view' ក្នុង urls.py
        
    return redirect('home')