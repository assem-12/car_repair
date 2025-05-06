from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/sell/', views.SellProductAPIView.as_view(), name='product-sell'),
    path('products/<int:pk>/buy/', views.BuyProductAPIView.as_view(), name='product-buy'),

    # Car Repair URLs
    path('services/', views.CarRepairListCreateAPIView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', views.CarRepairRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),

    # Service Request URLs
    path('requests/', views.ServiceRequestListCreateAPIView.as_view(), name='request-list-create'),
    path('requests/<int:pk>/', views.ServiceRequestRetrieveUpdateDestroyAPIView.as_view(), name='request-detail'),
    path('requests/<int:pk>/update-status/', views.UpdateServiceStatusAPIView.as_view(), name='request-update-status'),

    # Dashboard URLs
    path('dashboard/user/', views.UserDashboardAPIView.as_view(), name='user-dashboard'),
    path('dashboard/admin/', views.AdminDashboardAPIView.as_view(), name='admin-dashboard'),
]