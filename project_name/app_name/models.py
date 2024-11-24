from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_daily = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)  # Added category field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
 
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    food_item = models.ForeignKey(FoodItem, related_name="menu_items", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item.name} - Available: {self.is_available}"


class SpecialMenu(models.Model):
    food_item = models.ForeignKey(FoodItem, related_name="special_menu_items", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.food_item.name} - Special for {self.date}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def update_total_price(self):
        total = sum(item.total_price() for item in self.order_items.all())
        self.total_price = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.menu_item.food_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.food_item.name} x {self.quantity}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reservation_date = models.DateTimeField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.number_of_people} people - {self.reservation_date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    order = models.OneToOneField(Order, related_name="payment", on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=255, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class DeliveryPersonnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_assigned_orders(self):
        return Order.objects.filter(delivery_personnel=self)


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name="status_history", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Order.STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status change for Order #{self.order.id} to {self.status} at {self.updated_at}"


class SpecialMenuForm(models.Model):
    food_item = models.ForeignKey(FoodItem, related_name="special_menu_forms", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.food_item.name} for {self.date}"
