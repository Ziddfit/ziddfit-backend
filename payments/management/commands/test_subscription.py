import razorpay
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Gym
from Plan.models import Plan_config
import json


class Command(BaseCommand):
    help = 'Test Razorpay subscription creation'

    def add_arguments(self, parser):
        parser.add_argument('gym_id', type=str, help='UUID of gym to subscribe')
        parser.add_argument('plan_type', type=str, choices=['starter', 'pro', 'enterprise'],
                            help='Subscription plan type')

    def handle(self, *args, **options):
        gym_id = options['gym_id']
        plan_type = options['plan_type']

        # Verify gym exists
        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Gym with ID {gym_id} not found'))
            return

        # Verify plan exists
        try:
            plan = Plan_config.objects.get(tier=plan_type)
        except Plan_config.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Plan {plan_type} not found'))
            return

        self.stdout.write(f'Gym: {gym.name} ({gym_id})')
        self.stdout.write(f'Plan: {plan_type} - ₹{plan.price}')

        # Razorpay plan mapping
        plan_ids = {
            'starter': 'plan_PASTE_RAZORPAY_STARTER_ID',
            'pro': 'plan_PASTE_RAZORPAY_PRO_ID',
            'enterprise': 'plan_PASTE_RAZORPAY_ENTERPRISE_ID',
        }

        plan_id = plan_ids[plan_type]

        if 'PASTE' in plan_id:
            self.stdout.write(self.style.ERROR(
                'ERROR: Replace plan IDs from Razorpay dashboard in this file'
            ))
            self.stdout.write(self.style.WARNING(
                'Go to Dashboard → Subscriptions → Plans, copy plan IDs and update the plan_ids dict'
            ))
            return

        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            subscription_data = {
                'plan_id': plan_id,
                'total_count': 12,
                'quantity': 1,
                'customer_notify': 1,
                'notes': {
                    'gym_id': str(gym_id),
                    'plan_type': plan_type,
                }
            }

            self.stdout.write(self.style.WARNING('Creating subscription...'))
            subscription = client.subscription.create(data=subscription_data)

            self.stdout.write(self.style.SUCCESS('✓ Subscription created successfully!'))
            self.stdout.write(json.dumps(subscription, indent=2))

            self.stdout.write(self.style.SUCCESS(f'\n✓ Subscription ID: {subscription["id"]}'))
            self.stdout.write(self.style.SUCCESS(f'✓ Status: {subscription.get("status", "N/A")}'))
            self.stdout.write(self.style.SUCCESS(f'✓ Key ID: {settings.RAZORPAY_KEY_ID}'))

            self.stdout.write(self.style.WARNING('\nNext steps:'))
            self.stdout.write('1. Use the subscription_id with Razorpay checkout on frontend')
            self.stdout.write('2. Webhook will be triggered with subscription.activated event')
            self.stdout.write('3. Gym will be marked is_active=True in database')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating subscription: {str(e)}'))
