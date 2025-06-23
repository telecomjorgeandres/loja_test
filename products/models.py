from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # Get the currently active user model

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
            return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) # Will be useful later

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
