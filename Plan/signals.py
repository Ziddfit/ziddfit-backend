from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Plan_config,Plan_Subcription
from django.contrib.auth import get_user_model

user = get_user_model()

@receiver(post_save,sender = user)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        free_plan, _ = Plan_config.objects.get_or_create(
            tier='free', 
            defaults={'monthly_price': 0}
        )
        Plan_Subcription.objects.create(user=instance, plan=free_plan)