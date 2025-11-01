from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Category, Product, StockMovement


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.INT)
    def get_product_count(self, obj):
        return obj.products.count()


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    needs_reorder = serializers.BooleanField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'category', 'category_name', 
            'price', 'stock_quantity', 'status', 
            'needs_reorder', 'is_in_stock', 'created_at'
        ]
        read_only_fields = ['created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    needs_reorder = serializers.BooleanField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'description', 'category', 
            'category_name', 'price', 'stock_quantity', 'reorder_level',
            'status', 'needs_reorder', 'is_in_stock', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_sku(self, value):
        if self.instance and self.instance.sku == value:
            return value
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("Product with this SKU already exists.")
        return value


class StockMovementSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_sku', 'product_name',
            'movement_type', 'quantity', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        product = data.get('product')
        movement_type = data.get('movement_type')
        quantity = data.get('quantity')

        if movement_type == 'out' and product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"Insufficient stock. Available: {product.stock_quantity}"
            )
        return data

    def create(self, validated_data):
        product = validated_data['product']
        movement_type = validated_data['movement_type']
        quantity = validated_data['quantity']

        # Update product stock
        if movement_type == 'in':
            product.stock_quantity += quantity
        elif movement_type == 'out':
            product.stock_quantity -= quantity
        elif movement_type == 'adjustment':
            product.stock_quantity = quantity

        product.save()
        return super().create(validated_data)


class StockUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True)