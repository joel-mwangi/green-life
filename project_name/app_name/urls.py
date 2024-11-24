from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # User authentication views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    
    # Order and menu views
    path('order/', views.place_order, name='order'),
    path('order/success/', views.order_success, name='order_success'),
    path('menu/', views.menu, name='menu'),
    path('add_special_menu/', views.add_special_menu, name='add_special_menu'),
    
    # Reservation views
    path('reservation/', views.reservation_view, name='reservation'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    
    # User profile views
    path('profile/', views.profile_view, name='profile'),
    
    # Order status update views
    path('order/update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    
    # Payment processing views
    path('payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/error/', views.payment_error, name='payment_error'),
    
    # Delivery personnel views
    path('assigned_orders/', views.assigned_orders, name='assigned_orders'),
    path('delivery/update_status/<int:order_id>/', views.update_delivery_status, name='update_delivery_status'),
]
