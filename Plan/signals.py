from django.dispatch import receiver
from django.db.models.signals import post_save  # ← was missing
from .models import Plan_config, Plan_Subcription
from owners.models import Owner


@receiver(post_save, sender=Owner)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        free_plan, _ = Plan_config.objects.get_or_create(
            tier='free',
            defaults={
                'price': 0,
                'duration_days': 0  # ← add this, 0 = unlimited/no expiry for free plan
            }
        )
        Plan_Subcription.objects.create(user=instance, plan=free_plan)