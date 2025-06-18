from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from bar_app.models import Beer, NyamaChoma

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField()
    table_number = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    def calculate_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, null=True, blank=True, on_delete=models.CASCADE)
    nyama_choma = models.ForeignKey(NyamaChoma, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # For nyama choma
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        if self.beer:
            return f"{self.beer.name} x {self.quantity}"
        elif self.nyama_choma:
            return f"{self.nyama_choma.name} x {self.weight_kg}kg"
        return f"Order Item #{self.id}"
    
    def get_item_name(self):
        if self.beer:
            return f"{self.beer.brand} {self.beer.name}"
        elif self.nyama_choma:
            return self.nyama_choma.name
        return "Unknown Item"
    
    def get_total_price(self):
        if self.beer:
            return self.unit_price * self.quantity
        elif self.nyama_choma:
            return self.unit_price * (self.weight_kg or Decimal('0'))
        return Decimal('0')
    
    def save(self, *args, **kwargs):
        # Set unit price automatically
        if self.beer and not self.unit_price:
            self.unit_price = self.beer.price
        elif self.nyama_choma and not self.unit_price:
            self.unit_price = self.nyama_choma.price_per_kg
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous Cart {self.session_key}"
    
    def get_total_price(self):
        total = Decimal('0')
        for item in self.items.all():
            total += item.get_total_price()
        return total
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, null=True, blank=True, on_delete=models.CASCADE)
    nyama_choma = models.ForeignKey(NyamaChoma, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.beer:
            return f"{self.beer.name} x {self.quantity}"
        elif self.nyama_choma:
            return f"{self.nyama_choma.name} x {self.weight_kg}kg"
        return f"Cart Item #{self.id}"
    
    def get_item_name(self):
        if self.beer:
            return f"{self.beer.brand} {self.beer.name}"
        elif self.nyama_choma:
            return self.nyama_choma.name
        return "Unknown Item"
    
    def get_unit_price(self):
        if self.beer:
            return self.beer.price
        elif self.nyama_choma:
            return self.nyama_choma.price_per_kg
        return Decimal('0')
    
    def get_total_price(self):
        if self.beer:
            return self.beer.price * self.quantity
        elif self.nyama_choma:
            return self.nyama_choma.price_per_kg * (self.weight_kg or Decimal('0'))
        return Decimal('0')
