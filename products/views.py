from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, CarRepair, ServiceRequest
from .serializers import (
    ProductSerializer,
    SellProductSerializer,
    BuyProductSerializer,
    CarRepairSerializer,
    ServiceRequestSerializer,
    ServiceRequestUpdateSerializer
)
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly

# Product Views
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save()

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Product Operations
class SellProductAPIView(generics.UpdateAPIView):
    serializer_class = SellProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_active=True)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data["quantity"]
                if product.sell(quantity):
                    return Response({"message": f"Sold {quantity} items"}, status=status.HTTP_200_OK)
                return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class BuyProductAPIView(generics.UpdateAPIView):
    serializer_class = BuyProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_active=True)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data["quantity"]
                product.buy(quantity)
                return Response({"message": f"Added {quantity} items to stock"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

# Car Repair Views
class CarRepairListCreateAPIView(generics.ListCreateAPIView):
    queryset = CarRepair.objects.filter(is_active=True)
    serializer_class = CarRepairSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['service_name', 'description']

class CarRepairRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Service Request Views
class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    ordering_fields = ['created_at', 'total_price']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ServiceRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequest.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class UpdateServiceStatusAPIView(generics.UpdateAPIView):
    serializer_class = ServiceRequestUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    queryset = ServiceRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# Dashboard Views
class UserDashboardAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'active_requests': ServiceRequest.objects.filter(
                user=user
            ).exclude(status__in=['completed', 'cancelled']).count(),
            'completed_requests': ServiceRequest.objects.filter(
                user=user,
                status='completed'
            ).count(),
            'pending_payments': ServiceRequest.objects.filter(
                user=user,
                payment_status='unpaid'
            ).count(),
            'recent_requests': ServiceRequestSerializer(
                ServiceRequest.objects.filter(user=user).order_by('-created_at')[:5],
                many=True
            ).data
        }
        return Response(data)

class AdminDashboardAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        data = {
            'total_requests': ServiceRequest.objects.count(),
            'pending_requests': ServiceRequest.objects.filter(
                status='pending'
            ).count(),
            'in_progress_requests': ServiceRequest.objects.filter(
                status='in_progress'
            ).count(),
            'unpaid_requests': ServiceRequest.objects.filter(
                payment_status='unpaid'
            ).count(),
            'recent_requests': ServiceRequestSerializer(
                ServiceRequest.objects.all().order_by('-created_at')[:10],
                many=True
            ).data,
            'low_stock_products': ProductSerializer(
                Product.objects.filter(stock__lt=5, is_active=True),
                many=True
            ).data
        }
        return Response(data)