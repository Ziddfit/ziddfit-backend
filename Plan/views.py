from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import Plan_config, Plan_Subcription
from .serializer import Plan_con_Serializer, Plan_sub_Serializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_plan(request):
    try:
        plans = Plan_config.objects.all().order_by('price') 
        serializer = Plan_con_Serializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},                                
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])                     
def get_sub_status(request):
    try:
        subscription = Plan_Subcription.objects.select_related('plan').get(
            user=request.user
        )
        serializer = Plan_sub_Serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Plan_Subcription.DoesNotExist:
        return Response(
            {"error": "No subscription found for this user."},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_plan(request):
    tier = request.data.get('tier')

    # 1. Validate input
    if not tier:
        return Response(
            {"error": "tier is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. Find the requested plan
    try:
        new_plan = Plan_config.objects.get(tier=tier)
    except Plan_config.DoesNotExist:
        return Response(
            {"error": f"Plan '{tier}' does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        subscription = Plan_Subcription.objects.select_related('plan').get(
            user=request.user
        )
    except Plan_Subcription.DoesNotExist:
        return Response(
            {"error": "No subscription found. Contact support."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 4. Block if already on this plan
    if subscription.plan == new_plan and subscription.is_active:
        return Response(
            {"error": f"You are already on the {tier} plan."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 5. Calculate new expiry
    new_expiry = timezone.now() + timedelta(days=new_plan.duration_days)

    subscription.plan        = new_plan
    subscription.is_active   = True
    subscription.start_date  = timezone.now()
    subscription.expiry_date = new_expiry
    subscription.save()

    return Response({
        "message":  f"Successfully upgraded to {tier}.",
        "plan":     tier,
        "expires":  new_expiry,
    }, status=status.HTTP_200_OK)