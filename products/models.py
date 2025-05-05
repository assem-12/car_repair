from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def sell(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False

    def buy(self, quantity):
        self.stock += quantity
        self.save()


class CarRepair(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    car_repair = models.ForeignKey(CarRepair, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='unpaid')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        total = 0
        if self.product:
            total += self.product.price * self.quantity
        if self.car_repair:
            total += self.car_repair.price
        return total

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
