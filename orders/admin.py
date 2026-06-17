from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'qty', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total', 'created_at')
    fieldsets = (
        ('Order Info', {'fields': ('user', 'total', 'status', 'created_at')}),
        ('Shipping Info', {'fields': ('full_name', 'phone', 'address', 'city')}),
    )
