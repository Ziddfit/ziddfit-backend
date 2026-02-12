from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status

from models import Plan_config,Plan_Subcription
from serializer import Plan_con_Serializer,Plan_sub_Serializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_plan(request):
    try:
        plans = Plan_config.objects.all().order_by('monthly_price')
        serializer = Plan_con_Serializer(plans,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response("Error : {e}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sub_status(request):
    try:
        curr_plan = Plan_Subcription.objects.select_related('plan').get(user=request.user)
        serializer = Plan_sub_Serializer(curr_plan)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Plan_Subcription.DoesNotExist:
        return Response(
            {"error": "No subscription found for this user."}, 
            status=status.HTTP_404_NOT_FOUND
        )
