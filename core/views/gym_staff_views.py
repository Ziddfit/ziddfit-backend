from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from core.models.gym import Gym
from core.models.gym_staff import GymStaff
from core.serializers.gym_staff_serializer import GymStaffSerializer
from utils.pagination import StandardResultsPagination
@api_view(['GET', 'POST'])
def staff_list(request):
    # -------- GET: List staff for owner's gyms --------
    if request.method == 'GET':
        try:
            staff = GymStaff.objects.filter(gym__owner=request.user)
            paginator = StandardResultsPagination()
            paginated_qs = paginator.paginate_queryset(staff, request)

            serializer = GymStaffSerializer(paginated_qs, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Retrieval failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -------- POST: Create staff --------
    elif request.method == 'POST':
        try:
            serializer = GymStaffSerializer(data=request.data)
            if serializer.is_valid():
                gym = serializer.validated_data.get('gym')

                # Permission check: owner only
                if gym.owner != request.user:
                    return Response(
                        {"error": "You do not have permission to add staff to this gym."},
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
def staff_detail(request, pk):
    try:
        staff = get_object_or_404(
            GymStaff,
            pk=pk,
            gym__owner=request.user
        )

    except Exception as e:
        return Response(
            {"error": "Staff not found", "details": str(e)},
            status=status.HTTP_404_NOT_FOUND
        )

    # -------- GET: Retrieve --------
    if request.method == 'GET':
        serializer = GymStaffSerializer(staff)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------- PUT / PATCH: Update --------
    elif request.method in ['PUT', 'PATCH']:
        try:
            serializer = GymStaffSerializer(
                staff,
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

    # -------- DELETE: Remove --------
    elif request.method == 'DELETE':
        try:
            staff.delete()
            return Response(
                {"message": "Staff deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {"error": "Deletion failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
