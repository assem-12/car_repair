from django.urls import path
from .views import (
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    SellProductAPIView, BuyProductAPIView,
    CarRepairListCreateAPIView, CarRepairRetrieveUpdateDestroyAPIView,    ServiceRequestListCreateAPIView,
    ServiceRequestRetrieveUpdateDestroyAPIView,
    UpdateServiceStatusAPIView,
)

urlpatterns = [
    # Product APIs
    path('products/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/sell/', SellProductAPIView.as_view(), name='sell-product'),
    path('products/<int:pk>/buy/', BuyProductAPIView.as_view(), name='buy-product'),
    path('services/', ServiceRequestListCreateAPIView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceRequestRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
    path('services/<int:pk>/update-status/', UpdateServiceStatusAPIView.as_view(), name='service-status-update'),
    # Car Repair APIs
    path('car-repairs/', CarRepairListCreateAPIView.as_view(), name='car-repair-list'),
    path('car-repairs/<int:pk>/', CarRepairRetrieveUpdateDestroyAPIView.as_view(), name='car-repair-detail'),
]
