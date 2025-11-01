from django.contrib import admin
from .models import Category, Product, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'price', 'stock_quantity', 'status', 'needs_reorder']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['sku', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

    fieldsets = (
        ('Basic Information', {
            'fields': ('sku', 'name', 'description', 'category', 'status')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'reorder_level')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def needs_reorder(self, obj):
        return obj.needs_reorder
    needs_reorder.boolean = True
    needs_reorder.short_description = 'Needs Reorder'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__sku', 'product__name', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'