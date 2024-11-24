from django import forms
from .models import FoodItem, MenuItem, SpecialMenu, Order, OrderItem, Reservation, UserProfile, Payment, DeliveryPersonnel, OrderStatusHistory

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'is_daily']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['food_item', 'is_available']

class SpecialMenuForm(forms.ModelForm):
    class Meta:
        model = SpecialMenu
        fields = ['food_item', 'date']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'status']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'menu_item', 'quantity']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['user', 'number_of_people', 'reservation_date', 'special_requests']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'address', 'profile_picture']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'stripe_payment_id', 'amount_paid']

class DeliveryPersonnelForm(forms.ModelForm):
    class Meta:
        model = DeliveryPersonnel
        fields = ['user', 'phone_number', 'is_active']

class OrderStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderStatusHistory
        fields = ['order', 'status']
