from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import STATUS_CHOICES

class User(AbstractUser):
    wallet = models.DecimalField(max_digits=7,decimal_places=2,default=10000)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.IntegerField()

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Refund(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='refunds')
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

