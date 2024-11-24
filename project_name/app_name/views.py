from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from datetime import date

# Forms
from .forms import ReservationForm, UserProfileForm, OrderForm, PaymentForm, SpecialMenuForm

# Models
from .models import FoodItem, MenuItem, Order, OrderItem, DeliveryPersonnel, UserProfile, SpecialMenu


def home(request):
    return render(request, "app_name/home.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create the user
        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")  # Redirect to the login page after registration

    return render(request, "app_name/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(
                "home"
            )  # Redirect to the homepage or a dashboard after login
        else:
            messages.error(request,"Invalid username or password. Please ensure you are registered." )

    return render(request, "app_name/login.html")

@login_required
def place_order(request):
    form = OrderForm()  # Initialize the form
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            total_price = 0

            # Loop through each item submitted in the order form
            for key, value in request.POST.items():
                if key.startswith("item_"):  # Assuming item IDs are named like "item_1", "item_2", etc.
                    item_id = key.split("_")[1]
                    try:
                        menu_item = MenuItem.objects.get(id=item_id)
                        quantity = int(value)
                        if quantity > 0:
                            OrderItem.objects.create(
                                order=order, 
                                menu_item=menu_item, 
                                quantity=quantity
                            )
                            total_price += menu_item.price * quantity
                    except MenuItem.DoesNotExist:
                        continue  # Ignore if the item doesn't exist

            order.total_price = total_price
            order.save()

            return redirect("order_success")  # Redirect to success page
        else:
            messages.error(request, "There was an error in your order. Please try again.")

    menu_items = MenuItem.objects.all()
    return render(request, "app_name/order.html", {"form": form, "menu_items": menu_items})
@login_required
def reservation_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Link reservation to the logged-in user
            reservation.save()
            messages.success(request, "Your reservation has been successfully made!")
            return redirect("reservation_success")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReservationForm()

    return render(request, "app_name/reservation.html", {"form": form})


def reservation_success(request):
    return render(request, "app_name/reservation_success.html")

@login_required
def profile_view(request):
    user_profile, form= UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, "app_name/profile.html", {"form": form})


# View to display the menu (daily items + today's special menu items)
def menu(request):
    daily_food_items = FoodItem.objects.filter(is_daily=True)
    special_menu_items = SpecialMenu.objects.filter(date=date.today())

    return render(request, 'app_name/menu.html', {
        'daily_food_items': daily_food_items,
        'special_menu_items': special_menu_items,
    })

# View to add a special food item to the menu for today
def add_special_menu(request):
    if request.method == 'POST':
        form = SpecialMenuForm(request.POST)
        if form.is_valid():
            special_menu = form.save(commit=False)
            special_menu.date = date.today()  # Ensure the food item is added for today's date
            special_menu.save()
            return redirect('menu')  # Redirect to the menu page after adding
    else:
        form = SpecialMenuForm()

    return render(request, 'app)name/add_special_menu.html', {'form': form})
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()

            # Notify the customer
            notify_customer(order)

            return redirect("order_success")  # Redirect to a success page

    return render(request, "app_name/update_order_status.html", {"order": order})


def notify_customer(order):
    subject = "Your Order Status has been Updated"
    message = (
        "Hello "
        + order.customer_name
        + "\n\nYour order status has been updated to:"
        + order.get_status_display()
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.customer_email]

    send_mail(subject, message, email_from, recipient_list)
    # Implement email or SMS notification logic here
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def process_payment(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["stripeToken"]
            amount = int(order.total_price * 100)  # Convert to cents

            try:
                # Create a Stripe charge
                stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    description="Payment for Order #" + str(order.id),
                    source=token,
                )
                # After successful payment, mark the order as paid
                order.status = "paid"
                order.save()

                messages.success(request, "Payment successful!")
                return redirect("payment_success")  # Redirect to payment success page

            except stripe.error.StripeError as e:
                # Handle Stripe errors
                messages.error(request, f"Payment failed: {e.user_message}")
                return redirect("payment_error")  # Redirect to error page

    else:
        form = PaymentForm(initial={"amount": order.total_price})

    return render(request, "app_name/process_payment.html", {"form": form, "order": order})

def payment_success(request):
    return render(request, "app_name/payment_success.html")
def payment_error(request):
    return render(request, "app_name/payment_error.html")


def assigned_orders(request):
    delivery_person = get_object_or_404(DeliveryPersonnel, user=request.user)
    orders = Order.objects.filter(delivery_personnel=delivery_person)
    return render(request, "app_name/assigned_orders.html", {"orders": orders})

@login_required
def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("assigned_orders")

    return render(request, "app_name/update_status.html", {"order": order})
def order_success(request):
    return render(request, "app_name/order_success.html")
