from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from rest_framework.response import Response
from core.models.attendance import GymAttendance
from core.models.gym import Gym
from core.models.members import GymMember
from core.serializers.attendance import GymAttendanceSerializer

@api_view(['GET','POST'])
def attendance_list(request):
    """
    GET: List all attendances with filters (gym_id, member_id, date_from, date_to, entry_source)
    POST: Create new attendance record
    """
    if request.method == 'GET':
        try:
            attendances = GymAttendance.objects.filter(gym__owner=request.user).select_related('user', 'gym')
            gym_id = request.query_params.get('gym_id')
            if gym_id:
                attendances = attendances.filter(user_id=member_id)

            member_id = request.query_params.get('member_id')
            if member_id:
                attendances = attendances.filer(user_id=member_id)

            date_from = request.query_params.get('date_from')
            if date_from:
                try:
                    date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                    attendances = attendances.filter(checkin_Time__gte=date_from_obj)
                except ValueError:
                    pass

            date_to = request.query_params.get('date_to')
            if date_to:
                try:
                    date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                    date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
                    attendances = attendances.filter(checkin_Time__lte=date_to_obj)
                except ValueError:
                    pass  

            entry_source = request.query_params.get('entry_source')
            if entry_source:
                attendances = attendances.filter(entry_source=entry_source)

            serializer = GymAttendanceSerializer(attendances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        except Exception as e:
            return Response(
                {'error': 'Retrieval failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    elif request.method == 'POST':
        try:
            serializer = GymAttendanceSerializer(data=request.data)
            if serializer.is_valid():

                gym = serializer.validated_data.get('gym')

                if gym.owner != request.user:
                    return Response(
                        {"error": "You do not own this gym"},
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

@api_view(['GET', 'PUT', 'DELETE'])
def attendance_detail(request, attendance_id):
    """
    GET: Retrieve single attendance record
    PUT: Update attendance record (entry_source only)
    DELETE: Delete attendance record
    """

    attendance = get_object_or_404(GymAttendance,pk=attendance_id, gym__owner=request.user)

    if request.method == 'GET':
        serializer = GymAttendanceSerializer(attendance)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = GymAttendanceSerializer(attendance, data=request.data,  partial=True) 
        if serializer.is_valid():
            serializer.save(gym=attendance.gym,  user=attendance.user)
        return Response(serializer.data)  

    if request.method == 'DELETE':
        attendance.delete()
        return Response(
            {"message": "Attendance record deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )    

@api_view(['POST'])
def attendance_checkin(request):
    """
    POST:
    {
        "user_id": "uuid",
        "gym_id": "uuid",
        "entry_source": "QR_SCAN"
    }
    """
    try:
        user_id = request.data.get('user_id')
        gym_id = request.data.get('gym_id')
        entry_source = request.data.get('entry_source', 'QR_SCAN')

        if not user_id or not gym_id:
            return Response(
                {'error': 'user_id and gym_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)
        member = get_object_or_404(GymMember, pk=user_id, gym=gym)

        attendance = GymAttendance.objects.create(gym=gym, user=member, entry_source=entry_source)
        serializer = GymAttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": "Check-in failed", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )    
@api_view(['GET'])
def attendance_today(request):
    """
    GET: /attendances/today/?gym_id=<uuid>
    """

    try:
        gym_id = request.query_params.get('gym_id')
        if not gym_id:
            return Response(
                {'error': 'gym_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)

        today_start = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        attendances = GymAttendance.objects.filter(
            gym=gym,
            checkin_Time__gte=today_start
        ).select_related('user', 'gym').order_by('-checkin_Time')

        serializer = GymAttendanceSerializer(attendances, many=True)

        return Response(
            {
                'count': attendances.count(),
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {'error': 'Retrieval failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def attendance_stats(request):
    """
    GET: /attendances/stats/?gym_id=<uuid>&days=7
    """

    try:
        gym_id = request.query_params.get('gym_id')
        if not gym_id:
            return Response(
                {'error': 'gym_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)

        days = int(request.query_params.get('days', 7))
        date_from = timezone.now() - timedelta(days=days)

        queryset = GymAttendance.objects.filter(
            gym=gym,
            checkin_Time__gte=date_from
        )

        total_checkins = queryset.count()
        unique_members = queryset.values('user').distinct().count()

        checkins_by_source = queryset.values(
            'entry_source'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        daily_breakdown = []

        for i in range(days):
            day = timezone.now() - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)

            count = queryset.filter(
                checkin_Time__gte=day_start,
                checkin_Time__lte=day_end
            ).count()

            daily_breakdown.append({
                'date': day.strftime('%Y-%m-%d'),
                'checkins': count
            })

        return Response(
            {
                'total_checkins': total_checkins,
                'unique_members': unique_members,
                'checkins_by_source': list(checkins_by_source),
                'daily_breakdown': daily_breakdown
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {'error': 'Stats retrieval failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
