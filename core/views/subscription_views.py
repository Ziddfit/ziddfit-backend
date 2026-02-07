from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from core.models.subscription import GymSubscription
from core.models.members import GymMember
from core.serializers.subscription_serializer import GymSubscriptionSerializer


@api_view(['GET', 'POST'])
def subscription_list(request):

    # -------- GET: List subscriptions (owner gyms only) --------
    if request.method == 'GET':
        try:
            subscriptions = GymSubscription.objects.filter(
                member__gym__owner=request.user
            )
            serializer = GymSubscriptionSerializer(subscriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Retrieval failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------- POST: Create subscription --------
    elif request.method == 'POST':
        try:
            serializer = GymSubscriptionSerializer(data=request.data)
            if serializer.is_valid():

                member = serializer.validated_data.get('member')

                # Permission check
                if member.gym.owner != request.user:
                    return Response(
                        {"error": "You do not have permission to assign subscription to this member."},
                        status=status.HTTP_403_FORBIDDEN
                    )

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Creation failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def subscription_detail(request, pk):

    try:
        subscription = get_object_or_404(
            GymSubscription,
            pk=pk,
            member__gym__owner=request.user
        )
    except Exception as e:
        return Response(
            {"error": "Subscription not found", "details": str(e)},
            status=status.HTTP_404_NOT_FOUND
        )

    # -------- GET --------
    if request.method == 'GET':
        serializer = GymSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------- PUT / PATCH --------
    elif request.method in ['PUT', 'PATCH']:
        try:
            serializer = GymSubscriptionSerializer(
                subscription,
                data=request.data,
                partial=(request.method == 'PATCH')
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Update failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------- DELETE --------
    elif request.method == 'DELETE':
        try:
            subscription.delete()
            return Response(
                {"message": "Subscription deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {"error": "Deletion failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
