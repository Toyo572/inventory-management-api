from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend



from .models import Category, Product, StockMovement
from .serializers import (
    CategorySerializer, 
    ProductListSerializer, 
    ProductDetailSerializer,
    StockMovementSerializer,
    StockUpdateSerializer
)


@extend_schema(tags=['Categories'])
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


@extend_schema(tags=['Categories'])
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Products'])
class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    Supports filtering by category, status, and stock availability.
    """
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductDetailSerializer
        return ProductListSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by category ID'
            ),
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by status (active, inactive, discontinued)'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search in name, SKU, or description'
            ),
            OpenApiParameter(
                name='low_stock',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter products that need reorder'
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        low_stock = self.request.query_params.get('low_stock')
        
        if low_stock and low_stock.lower() == 'true':
            queryset = [p for p in queryset if p.needs_reorder]
            
        return queryset


@extend_schema(tags=['Products'])
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product.
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Stock Management'])
class StockMovementListCreateView(generics.ListCreateAPIView):
    """
    List all stock movements or create a new stock movement.
    """
    queryset = StockMovement.objects.select_related('product').all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'movement_type']
    ordering_fields = ['created_at']

    @extend_schema(
        examples=[
            OpenApiExample(
                'Stock In Example',
                value={
                    'product': 1,
                    'movement_type': 'in',
                    'quantity': 50,
                    'notes': 'Received from supplier'
                },
                request_only=True
            ),
            OpenApiExample(
                'Stock Out Example',
                value={
                    'product': 1,
                    'movement_type': 'out',
                    'quantity': 10,
                    'notes': 'Sold to customer'
                },
                request_only=True
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Stock Management'])
class ProductStockInView(APIView):
    """
    Add stock to a product.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=StockUpdateSerializer,
        responses={200: StockMovementSerializer},
        examples=[
            OpenApiExample(
                'Add Stock Example',
                value={
                    'quantity': 100,
                    'notes': 'Restocking from warehouse'
                },
                request_only=True
            )
        ]
    )
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StockUpdateSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            notes = serializer.validated_data.get('notes', '')

            movement = StockMovement.objects.create(
                product=product,
                movement_type='in',
                quantity=quantity,
                notes=notes
            )

            product.stock_quantity += quantity
            product.save()

            return Response(
                StockMovementSerializer(movement).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Stock Management'])
class ProductStockOutView(APIView):
    """
    Remove stock from a product.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=StockUpdateSerializer,
        responses={200: StockMovementSerializer},
        examples=[
            OpenApiExample(
                'Remove Stock Example',
                value={
                    'quantity': 5,
                    'notes': 'Product sold'
                },
                request_only=True
            )
        ]
    )
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StockUpdateSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            notes = serializer.validated_data.get('notes', '')

            if product.stock_quantity < quantity:
                return Response(
                    {'error': f'Insufficient stock. Available: {product.stock_quantity}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            movement = StockMovement.objects.create(
                product=product,
                movement_type='out',
                quantity=quantity,
                notes=notes
            )

            product.stock_quantity -= quantity
            product.save()

            return Response(
                StockMovementSerializer(movement).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Products'])
class LowStockProductsView(generics.ListAPIView):
    """
    List all products that need reordering (stock at or below reorder level).
    """
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.select_related('category').filter(
            stock_quantity__lte=models.F('reorder_level')
        )