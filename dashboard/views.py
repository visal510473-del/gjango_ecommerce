from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from products.models import Product, ProductVariant
from decimal import Decimal
from django.db.models.functions import TruncMonth, TruncDay, TruncYear
from django.db.models import Sum
import functools


def staff_required(view_func):
    @functools.wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@staff_required
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    new_orders_count = orders.filter(notified=False).count()
    new_orders_qs = orders.filter(notified=False)
    new_orders_ids = list(new_orders_qs.values_list('id', flat=True))
    if new_orders_count:
        orders.filter(notified=False).update(notified=True)
        new_orders_qs.update(notified=True)
    total_sales = sum(o.total for o in orders)
    total_orders = orders.count()
    total_customers = User.objects.filter(is_staff=False).count()
    total_profit = total_sales * Decimal('0.35')

    recent_orders = orders[:5]
    # show latest products first to match the storefront
    products = Product.objects.all().order_by('-created_at')

    # accurate low stock
    low_stock = Product.objects.filter(stock__lte=10).order_by('stock')[:4]

    # compute top selling products (all-time)
    top_qs_all = (
        OrderItem.objects
        .values('product')
        .annotate(total_sold=Sum('qty'))
        .order_by('-total_sold')[:5]
    )
    top_products_all = []
    for item in top_qs_all:
        try:
            prod = Product.objects.get(id=item['product'])
            top_products_all.append({'product': prod, 'sold': item['total_sold']})
        except Product.DoesNotExist:
            continue
    # fallback: if no sales yet, show latest products
    if not top_products_all:
        latest_products = Product.objects.order_by('-created_at')[:5]
        top_products_all = [{'product': p, 'sold': 0} for p in latest_products]

    # compute top selling products from recent orders (last 20)
    recent_orders_for_top = orders[:20]
    top_qs_recent = (
        OrderItem.objects
        .filter(order__in=recent_orders_for_top)
        .values('product')
        .annotate(total_sold=Sum('qty'))
        .order_by('-total_sold')[:5]
    )
    # build list of dicts with product and sold count, preserving order
    top_products_recent = []
    for item in top_qs_recent:
        try:
            prod = Product.objects.get(id=item['product'])
            top_products_recent.append({'product': prod, 'sold': item['total_sold']})
        except Product.DoesNotExist:
            continue
    # fallback: if no recent sales, empty list (template will show message)
    if not top_products_recent:
        # fallback to same as all-time when recent has none — keep same dict shape
        top_products_recent = [{'product': p, 'sold': 0} for p in top_products_all[:5]]
    
    # also compute top variants in recent orders (if variants recorded)
    top_variants_recent = []
    top_qs_variants = (
        OrderItem.objects
        .filter(order__in=recent_orders_for_top, variant__isnull=False)
        .values('variant')
        .annotate(total_sold=Sum('qty'))
        .order_by('-total_sold')[:5]
    )
    for item in top_qs_variants:
        try:
            variant = ProductVariant.objects.get(id=item['variant'])
            top_variants_recent.append({'variant': variant, 'sold': item['total_sold']})
        except ProductVariant.DoesNotExist:
            continue

    period = request.GET.get('period', 'month')
    if period == 'day':
        trunc = TruncDay('created_at')
        label_fmt = '%d %b'
    elif period == 'year':
        trunc = TruncYear('created_at')
        label_fmt = '%Y'
    else:
        trunc = TruncMonth('created_at')
        label_fmt = '%b %Y'

    agg = (
        Order.objects
        .annotate(period=trunc)
        .values('period')
        .annotate(total=Sum('total'))
        .order_by('period')
    )

    sales_labels = [item['period'].strftime(label_fmt) for item in agg if item['period']]
    sales_data = [float(item['total']) for item in agg]

    sales_series = [{'label': lbl, 'value': val} for lbl, val in zip(sales_labels, sales_data)]
    max_sales = max(sales_data) if sales_data else 1

    return render(request, 'dashboard/index.html', {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_profit': total_profit,
        'new_orders_count': new_orders_count,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
        'top_products': top_products_all,
        'top_products_all': top_products_all,
        'top_products_recent': top_products_recent,
        'products': products,
        'sales_labels': sales_labels,
        'sales_data': sales_data,
        'sales_series': sales_series,
        'max_sales': max_sales,
        'period': period,
        'new_orders_ids': new_orders_ids,
        'active_tab': 'dashboard',
    })


@staff_required
def update_stock(request, product_id):
    if request.method == 'POST':
        try:
            add_amount = int(request.POST.get('add_stock', 0))
        except (TypeError, ValueError):
            add_amount = 0

        product = get_object_or_404(Product, id=product_id)
        # only allow positive increments
        if add_amount:
            product.stock = max(0, product.stock + add_amount)
            product.save()
            messages.success(request, f'Stock updated for "{product.name}".')

    return redirect('dashboard_products')

@staff_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock', 0)
        image = request.FILES.get('image')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image
        )

        colors = request.POST.getlist('color[]')
        storages = request.POST.getlist('storage[]')
        for color, storage in zip(colors, storages):
            if color and storage:
                ProductVariant.objects.create(
                    product=product,
                    color=color,
                    storage=storage
                )

        messages.success(request, f'Product "{name}" added successfully!')
        return redirect('dashboard')
    
    return render(request, 'dashboard/add_product.html', {
        'active_tab': 'add_product'
    })

@staff_required
def dashboard_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/products.html', {
        'products': products,
        'active_tab': 'products'
    })

@staff_required
def dashboard_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/orders.html', {
        'orders': orders,
        'active_tab': 'orders'
    })


@staff_required
def dashboard_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.select_related('product', 'variant').all()
    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'items': items,
        'active_tab': 'orders'
    })

@staff_required
def dashboard_customers(request):
    customers = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, 'dashboard/customers.html', {
        'customers': customers,
        'active_tab': 'customers'
    })

@staff_required
def dashboard_low_stock(request):
    from products.models import Product
    low_stock = Product.objects.filter(stock__lte=10).order_by('stock')
    return render(request, 'dashboard/low_stock.html', {
        'low_stock': low_stock,
        'active_tab': 'low_stock'
    })

@staff_required
def manage_variants(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = ProductVariant.objects.filter(product=product)

    if request.method == 'POST':
        color = request.POST.get('color')
        storage = request.POST.get('storage')
        image = request.FILES.get('image')

        ProductVariant.objects.create(
            product=product,
            color=color,
            storage=storage,
            image=image
        )
        messages.success(request, f'Variant added successfully!')
        return redirect('manage_variants', product_id=product_id)

    return render(request, 'dashboard/manage_variants.html', {
        'product': product,
        'variants': variants,
        'active_tab': 'products'
    })

@staff_required
def delete_variant(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_id = variant.product.id
    variant.delete()
    messages.success(request, 'Variant deleted!')
    return redirect('manage_variants', product_id=product_id)

@staff_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product deleted successfully!')
    return redirect('dashboard_products')

@staff_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.stock = request.POST.get('stock')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        messages.success(request, f'{product.name} updated successfully!')
        return redirect('dashboard_products')
    return render(request, 'dashboard/edit_product.html', {
        'product': product,
        'active_tab': 'products'
    })