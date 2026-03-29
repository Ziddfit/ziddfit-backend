import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import hmac
import hashlib
from core.models import Gym
from Plan.models import Plan_config

class CreateSubscriptionView(APIView):
    def post(self, request):
        gym_id = request.data.get('gym_id')
        plan_type = request.data.get('plan_type')

        if not gym_id or not plan_type:
            return Response({'error': 'gym_id and plan_type are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan_config.objects.get(tier=plan_type)
        except Plan_config.DoesNotExist:
            return Response({'error': 'Invalid plan_type'}, status=status.HTTP_400_BAD_REQUEST)

        plan_ids = {
            'starter': 'plan_starter_id',  # Replace with actual plan_id from Razorpay
            'pro': 'plan_pro_id',
            'enterprise': 'plan_enterprise_id',
        }

        if plan_type not in plan_ids:
            return Response({'error': 'Invalid plan_type'}, status=status.HTTP_400_BAD_REQUEST)

        plan_id = plan_ids[plan_type]

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
            subscription = client.subscription.create(data=subscription_data)
            return Response({
                'subscription_id': subscription['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(APIView):
    def post(self, request):
        # Verify the signature
        razorpay_signature = request.headers.get('X-Razorpay-Signature')
        if not razorpay_signature:
            return Response({'error': 'Missing signature'}, status=status.HTTP_400_BAD_REQUEST)

        payload = request.body
        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(razorpay_signature, expected_signature):
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the payload
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        event = data.get('event')
        if event == 'subscription.activated':
            self.handle_subscription_activated(data)
        elif event == 'subscription.charged':
            self.handle_subscription_charged(data)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def handle_subscription_activated(self, data):
        subscription = data.get('payload', {}).get('subscription', {})
        notes = subscription.get('entity', {}).get('notes', {})
        gym_id = notes.get('gym_id')
        plan_type = notes.get('plan_type')

        if gym_id and plan_type:
            try:
                gym = Gym.objects.get(id=gym_id)
                plan = Plan_config.objects.get(tier=plan_type)
                gym.is_active = True
                gym.plan = plan
                gym.save()
            except (Gym.DoesNotExist, Plan_config.DoesNotExist):
                pass  # Log or handle

    def handle_subscription_charged(self, data):
        # Log successful monthly recurring payments
        # For now, just print or log
        print('Subscription charged:', data)