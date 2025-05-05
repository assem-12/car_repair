from rest_framework import serializers
from .models import Product, CarRepair, ServiceRequest

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SellProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class BuyProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class CarRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRepair
        fields = '__all__'
class ServiceRequestSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['status', 'payment_status', 'total_price', 'created_at']
