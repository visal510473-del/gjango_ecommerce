from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-products/', views.add_product, name='add_product'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('products/<int:product_id>/update-stock/', views.update_stock, name='update_stock'),
    path('orders/', views.dashboard_orders, name='dashboard_orders'),
    path('orders/<int:order_id>/', views.dashboard_order_detail, name='dashboard_order_detail'),
    path('customers/', views.dashboard_customers, name='dashboard_customers'),
    path('low-stock/', views.dashboard_low_stock, name='dashboard_low_stock'),
    path('products/<int:product_id>/variants/', views.manage_variants, name='manage_variants'),
    path('variants/<int:variant_id>/delete/', views.delete_variant, name='delete_variant'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
]
