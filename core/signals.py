from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.gym import Gym
from core.models.members import GymMember
from core.models.subscription import GymSubscription
from datetime import date, timedelta

@receiver(post_save, sender = Gym)
def create_default_plan(sender, instance, created, **kwargs):
    if created:
        GymSubscription.objects.create(
            gym=instance,
            plan_type='MONTHLY',
            time_period=30,
            price=0,
            description='Default free plan',
            is_default=True,
            is_active=True,
        )


#this fires up when a new gymmember is saved
@receiver(post_save, sender=GymMember)
def assign_default_plan(sender, instance, created, **kwargs):
    if created:
        if instance.subscription:
            # owner selected a plan — just calculate membership_end from it
            instance.membership_end = date.today() + timedelta(days=instance.subscription.time_period)
            instance.save(update_fields=['membership_end'])
        else:
            # no plan selected — assign default free plan
            default_plan = GymSubscription.objects.filter(
                gym=instance.gym,
                is_default=True,
                is_active=True
            ).first()

            if default_plan:
                instance.subscription = default_plan
                instance.membership_end = date.today() + timedelta(days=default_plan.time_period)
                instance.save(update_fields=['subscription', 'membership_end'])