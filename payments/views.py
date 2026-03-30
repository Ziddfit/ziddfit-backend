import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import hmac
import hashlib
from core.models import Gym, Transaction
from Plan.models import Plan_config

@api_view(['POST'])
def create_subscription(request):
    gym_id = request.data.get('gym_id')
    plan_type = request.data.get('plan_type')

    if not gym_id or not plan_type:
        return Response({'error': 'gym_id and plan_type are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        plan = Plan_config.objects.get(tier=plan_type)
    except Plan_config.DoesNotExist:
        return Response({'error': 'Invalid plan_type'}, status=status.HTTP_400_BAD_REQUEST)

    # Map plan types to Razorpay plan IDs
    # Get these from: https://dashboard.razorpay.com/app/subscriptions/plans (Test Mode)
    # Click on each plan and copy the Plan ID (format: plan_XXXXX)
    plan_ids = {
        'starter': 'plan_SXAKtAAeMr12DT',      # TODO: Replace with actual plan_id from Razorpay
        'pro': 'plan_pro_id',              # TODO: Replace with actual plan_id from Razorpay
        'enterprise': 'plan_enterprise_id', # TODO: Replace with actual plan_id from Razorpay
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


def verify_razorpay_signature(payload, signature):
    expected_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


@csrf_exempt
@api_view(['POST'])
def razorpay_webhook(request):
    razorpay_signature = request.headers.get('X-Razorpay-Signature')
    if not razorpay_signature:
        return Response({'error': 'Missing signature'}, status=status.HTTP_400_BAD_REQUEST)

    payload = request.body
    if not verify_razorpay_signature(payload, razorpay_signature):
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    event = data.get('event')
    if event == 'subscription.activated':
        handle_subscription_activated(data)
    elif event == 'subscription.charged':
        handle_subscription_charged(data)

    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


def handle_subscription_activated(data):
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
            pass


def handle_subscription_charged(data):
    invoice_payload = data.get('payload', {}).get('invoice', {})
    payment_payload = data.get('payload', {}).get('payment', {})
    subscription = data.get('payload', {}).get('subscription', {})

    amount_paid = None
    if payment_payload.get('entity'):
        amount_paid = payment_payload['entity'].get('amount')
    elif invoice_payload.get('entity'):
        amount_paid = invoice_payload['entity'].get('amount')

    if amount_paid is not None:
        amount_paid = int(amount_paid) / 100.0

    notes = subscription.get('entity', {}).get('notes', {})
    gym_id = notes.get('gym_id')
    plan_type = notes.get('plan_type')

    if not gym_id:
        return

    try:
        gym = Gym.objects.get(id=gym_id)
    except Gym.DoesNotExist:
        return

    try:
        Transaction.objects.create(
            name=f"Recurring subscription charged ({plan_type})",
            gym=gym,
            transaction_type='credit',
            amount=int(amount_paid * 100) if amount_paid is not None else 0,
            category='',
            party_name='Razorpay',
            party_type='other',
            metadata={
                'razorpay_event': data.get('event'),
                'subscription_id': subscription.get('entity', {}).get('id'),
                'amount_paid': amount_paid,
            },
        )
    except Exception:
        pass
