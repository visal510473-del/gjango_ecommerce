from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductVariant
from .models import Order, OrderItem


def parse_cart_key(cart_key):
    if isinstance(cart_key, str) and cart_key.startswith('variant:'):
        return 'variant', cart_key.split(':', 1)[1]
    if isinstance(cart_key, str) and cart_key.startswith('product:'):
        return 'product', cart_key.split(':', 1)[1]
    return 'product', cart_key


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('/cart/')

    cart_items = []
    grand_total = 0

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
                variant = None
            except Product.DoesNotExist:
                continue

        item_total = product.price * qty
        grand_total += item_total
        cart_items.append({
            'product':    product,
            'variant':    variant,
            'qty':        qty,
            'item_total': item_total,
        })

    if request.method == 'POST':
        # validate stock availability before creating order
        for item in cart_items:
            prod = item['product']
            qty = item['qty']
            if prod.stock < qty:
                messages.error(request, f'Insufficient stock for {prod.name}. Available: {prod.stock}')
                return redirect('cart_view')

        order = Order.objects.create(
            user      = request.user,
            total     = grand_total,
            status    = 'paid',
            notified  = False,
            full_name = request.POST.get('first_name', '') + ' ' + request.POST.get('last_name', ''),
            phone     = request.POST.get('phone', ''),
            address   = request.POST.get('address', ''),
            city      = request.POST.get('city', ''),
        )
            

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                variant=item.get('variant'),
                qty=item['qty'],
                price=item['product'].price
            )
            # decrement product stock
            prod = item['product']
            prod.stock = max(0, prod.stock - item['qty'])
            prod.save()

        request.session['cart'] = {}
        return render(request, 'orders/success.html', {'order': order})

    return render(request, 'orders/payment.html', {
        'cart_items':  cart_items,
        'grand_total': grand_total,
    })
