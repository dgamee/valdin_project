from django.contrib import admin
from .models import Client, Product, ProductImage, Category, CartOrder, CartOrderItems


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone_number',]

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['name','product_image','price']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'payment_status', 'order_date']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'item', 'image', 'quantity', 'price', 'total']

    

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
