from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
import datetime
from datetime import timedelta
from rest_framework.response import Response
from core.models.attendance import GymAttendance
from core.models.gym import Gym
from core.models.members import GymMember
from core.serializers.attendance_serializer import GymAttendanceSerializer

@api_view(['GET', 'POST'])
def attendance_list(request, gym_id):
    if request.method == 'GET':
        attendances = GymAttendance.objects.filter(
            gym_id=gym_id,
            gym__owner=request.user
        ).select_related('user', 'gym')

        member_id = request.query_params.get('member_id')
        if member_id:
            attendances = attendances.filter(user_id=member_id)

        date_from = request.query_params.get('date_from')
        if date_from:
            date_from_obj = timezone.make_aware(
                datetime.datetime.strptime(date_from, '%Y-%m-%d')
            )
            attendances = attendances.filter(checkin_Time__gte=date_from_obj)

        date_to = request.query_params.get('date_to')
        if date_to:
            date_to_obj = timezone.make_aware(
                datetime.datetime.strptime(date_to, '%Y-%m-%d')
            ).replace(hour=23, minute=59, second=59)
            attendances = attendances.filter(checkin_Time__lte=date_to_obj)

        entry_source = request.query_params.get('entry_source')
        if entry_source:
            attendances = attendances.filter(entry_source=entry_source)

        serializer = GymAttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = GymAttendanceSerializer(data=request.data)
    if serializer.is_valid():
        gym = get_object_or_404(Gym, id=gym_id, owner=request.user)
        serializer.save(gym=gym)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def attendance_detail(request, attendance_id):
    attendance = get_object_or_404(
        GymAttendance,
        pk=attendance_id,
        gym__owner=request.user
    )

    if request.method == 'GET':
        serializer = GymAttendanceSerializer(attendance)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = GymAttendanceSerializer(
            attendance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    attendance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def attendance_checkin(request):
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

    today = timezone.now().date()
    if GymAttendance.objects.filter(
        gym=gym,
        user=member,
        checkin_time__date=today
    ).exists():
        return Response(
            {'error': 'Member already checked in today'},
            status=status.HTTP_400_BAD_REQUEST
        )

    attendance = GymAttendance.objects.create(
        gym=gym,
        user=member,
        entry_source=entry_source
    )
    serializer = GymAttendanceSerializer(attendance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def attendance_today(request, gym_id):
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
        {'count': attendances.count(), 'results': serializer.data},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def attendance_stats(request, gym_id):
    gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)
    days = int(request.query_params.get('days', 7))
    date_from = timezone.now() - timedelta(days=days)

    queryset = GymAttendance.objects.filter(
        gym=gym,
        checkin_time__gte=date_from
    )

    daily_breakdown = queryset.annotate(
        day=TruncDate('checkin_time')
    ).values('day').annotate(
        checkins=Count('id')
    ).order_by('-day')

    return Response({
        'total_checkins': queryset.count(),
        'unique_members': queryset.values('user').distinct().count(),
        'checkins_by_source': list(
            queryset.values('entry_source').annotate(count=Count('id'))
        ),
        'daily_breakdown': list(daily_breakdown)
    }, status=status.HTTP_200_OK)