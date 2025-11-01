from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    StockMovementListCreateView,
    ProductStockInView,
    ProductStockOutView,
    LowStockProductsView,
)

urlpatterns = [
    # Categories
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    
    # Products
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('api/products/low-stock/', LowStockProductsView.as_view(), name='low-stock-products'),
    
    # Stock Management
    path('api/stock-movements/', StockMovementListCreateView.as_view(), name='stock-movement-list-create'),
    path('api/products/<int:pk>/stock-in/', ProductStockInView.as_view(), name='product-stock-in'),
    path('api/products/<int:pk>/stock-out/', ProductStockOutView.as_view(), name='product-stock-out'),
]