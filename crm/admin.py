from django.contrib import admin
from .models import Customer, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'status', 'interest', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'phone', 'interest')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__full_name', 'product_details')