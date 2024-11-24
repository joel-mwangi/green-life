from django.contrib import admin
from .models import FoodItem, MenuItem, Order, OrderItem, DeliveryPersonnel, UserProfile, SpecialMenu, Reservation

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_daily', 'category', 'created_at')
    search_fields = ('name', 'price', 'category')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'is_available', 'created_at')
    list_filter = ('food_item__category', 'is_available')  # Filtering by category
    search_fields = ('food_item__name', 'food_item__category')  # Searching by category as well

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'total_price')
    search_fields = ('order__id', 'menu_item__name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'status')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')

class SpecialMenuAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'date')
    list_filter = ('date',)
    search_fields = ('food_item__name',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation_date', 'special_requests')
    list_filter = ('reservation_date',)
    search_fields = ('user__username',)

class DeliveryPersonnelAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_orders_count')
    search_fields = ('user__username',)

    def assigned_orders_count(self, obj):
        return obj.get_assigned_orders().count()

    assigned_orders_count.short_description = 'Assigned Orders'

admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SpecialMenu, SpecialMenuAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(DeliveryPersonnel, DeliveryPersonnelAdmin)
