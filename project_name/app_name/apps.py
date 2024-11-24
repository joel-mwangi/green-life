from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_name'
    
    
def create_default_food_item(sender, **kwargs):
    from .models import FoodItem
    # Check if the default item already exists
    if not FoodItem.objects.filter(name="Default Food Item").exists():
        # Create the default FoodItem
        FoodItem.objects.create(
            name="Default Food Item",
            description="A default food item.",
            price=10.00,
            is_daily=False
        )

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_name'

    def ready(self):
        post_migrate.connect(create_default_food_item, sender=self)
