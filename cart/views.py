from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductVariant


def build_cart_key(product_id=None, variant_id=None):
    if variant_id:
        return f'variant:{variant_id}'
    return f'product:{product_id}'


def parse_cart_key(cart_key):
    if isinstance(cart_key, str) and cart_key.startswith('variant:'):
        return 'variant', cart_key.split(':', 1)[1]
    if isinstance(cart_key, str) and cart_key.startswith('product:'):
        return 'product', cart_key.split(':', 1)[1]
    return 'product', cart_key


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0
    
    for cart_key, qty in cart.items():
        key_type, object_id = parse_cart_key(cart_key)

        if key_type == 'variant':
            try:
                variant = ProductVariant.objects.get(id=object_id)
                product = variant.product
                item_total = product.price * qty
                grand_total += item_total
                cart_items.append({
                    'product': product,
                    'variant': variant,
                    'qty': qty,
                    'item_total': item_total,
                    'key': cart_key,
                })
                continue
            except ProductVariant.DoesNotExist:
                pass

        try:
            product = Product.objects.get(id=object_id)
            item_total = product.price * qty
            grand_total += item_total
            cart_items.append({
                'product': product,
                'variant': None,
                'qty': qty,
                'item_total': item_total,
                'key': cart_key,
            })
        except Product.DoesNotExist:
            continue
            
    context = {
        'cart_items': cart_items,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    variant_id = request.POST.get('variant_id')
    key = build_cart_key(product_id=product_id, variant_id=variant_id)

    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    return redirect('/cart/')

def remove_from_cart(request, cart_key):
    cart = request.session.get('cart', {})
    if cart_key in cart:
        del cart[cart_key]
        request.session['cart'] = cart
    return redirect('/cart/')

@login_required
def checkout(request):
    from orders.models import Order, OrderItem
    
    cart = request.session.get('cart', {})
    order = Order.objects.create(user=request.user, total=0)
    total = 0

    for cart_key, qty in cart.items():
        key_type, object_id = parse_cart_key(cart_key)

        if key_type == 'variant':
            try:
                variant = ProductVariant.objects.get(id=object_id)
                product = variant.product
            except ProductVariant.DoesNotExist:
                continue
        else:
            try:
                product = Product.objects.get(id=object_id)
            except Product.DoesNotExist:
                continue

        item_total = product.price * qty
        total += item_total

        OrderItem.objects.create(
            order=order,
            product=product,
            qty=qty,
            price=product.price
        )

    order.total = total
    order.save()

    request.session['cart'] = {}

    return render(request, 'orders/success.html', {'order': order})