from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Product, CarRepair
from .serializers import ProductSerializer, SellProductSerializer, BuyProductSerializer, CarRepairSerializer
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
# Product CRUD API
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Sell Product API
class SellProductAPIView(generics.UpdateAPIView):
    serializer_class = SellProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data["quantity"]
            if product.sell(quantity):
                return Response({"message": f"Sold {quantity} items"}, status=status.HTTP_200_OK)
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Buy Product API
class BuyProductAPIView(generics.UpdateAPIView):
    serializer_class = BuyProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data["quantity"]
            product.buy(quantity)
            return Response({"message": f"Added {quantity} items to stock"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Car Repair CRUD API
class CarRepairListCreateAPIView(generics.ListCreateAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CarRepairRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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



class UpdateServiceStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, pk):
        try:
            service = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({"error": "Service request not found"}, status=404)

        status_ = request.data.get("status")
        payment_status = request.data.get("payment_status")

        if status_:
            service.status = status_
        if payment_status:
            service.payment_status = payment_status

        service.save()
        return Response({"message": "Service updated successfully"})
