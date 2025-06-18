from django.db import models
from django.contrib.auth.models import User

# Category model for both beer and nyama choma
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# Beer model with types and basic info
class Beer(models.Model):
    BEER_TYPES = [
        ('lager', 'Lager'),
        ('ale', 'Ale'),
        ('stout', 'Stout'),
        ('pilsner', 'Pilsner'),
        ('wheat', 'Wheat Beer'),
        ('ipa', 'IPA'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    beer_type = models.CharField(max_length=20, choices=BEER_TYPES)
    alcohol_content = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='beers/', blank=True)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='beers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} - {self.name}"


# Nyama Choma (Grilled Meat) model
class NyamaChoma(models.Model):
    MEAT_TYPES = [
        ('beef', 'Beef'),
        ('goat', 'Goat'),
        ('chicken', 'Chicken'),
        ('pork', 'Pork'),
        ('fish', 'Fish'),
        ('mutton', 'Mutton'),
    ]

    name = models.CharField(max_length=100)
    meat_type = models.CharField(max_length=20, choices=MEAT_TYPES)
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='nyama_choma/', blank=True)
    available = models.BooleanField(default=True)
    spice_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=3)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.meat_type})"


# Table model for reservations
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    location = models.CharField(max_length=100)  # indoor, outdoor, VIP

    class Meta:
        ordering = ['table_number']

    def __str__(self):
        return f"Table {self.table_number} ({self.location})"


# Reservation model
class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    party_size = models.IntegerField()
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.customer_name} - Table {self.table.table_number} on {self.date}"
