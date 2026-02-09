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
from core.pagination import StandardResultsPagination


@api_view(['GET', 'POST'])
def attendance_list(request, gym_id):
    if request.method == 'GET':
        attendances = GymAttendance.objects.filter(
            gym_id=gym_id,
            gym__owner=request.user
        ).select_related('member', 'gym')

        member_id = request.query_params.get('member_id')
        if member_id:
            attendances = attendances.filter(member_id=member_id)

        date_from = request.query_params.get('date_from')
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                attendances = attendances.filter(date__gte=date_from)
            except ValueError:
                    return Response(
                        {
                            'error': 'Invalid date_from format',
                            'detail': 'Expected format: YYYY-MM-DD (e.g., 2025-02-01)',
                            'received': date_from
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    ) 
            
        date_to = request.query_params.get('date_to')
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                date_to_obj = date_to_obj.replace(hour = 23, minute = 59, second = 59)
                attendances = attendances.filter(date__lte=date_to)

            except ValueError:
                return Response(
                    {
                        'error': 'Invalid date_to format',
                        'detail': 'Expected format: YYYY-MM-DD (e.g., 2025-02-01)',
                        'received': date_to
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        if date_from and date_to:
            if date_from_obj > date_to_obj:
                return Response(
                    {
                        'error': 'Invalid date range',
                        'detail': 'date_from must be before or equal to date_to'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        entry_source = request.query_params.get('entry_source')
        if entry_source:
            attendances = attendances.filter(entry_source=entry_source)
        
        paginator = StandardResultsPagination(20, 100)
        paginated_qs = paginator.paginate_queryset(attendances, request)

        serializer = GymAttendanceSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method == 'POST':
        serializer = GymAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            gym = get_object_or_404(Gym, id=gym_id, owner=request.user)

            member_id = serializer.data.get('member_id')
            member = get_object_or_404(GymMember, pk=member_id, gym=gym)
            serializer.save(gym=gym, member = member)

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

from django.db import transaction, IntegrityError

@api_view(['POST'])
def attendance_checkin(request):
    member_id = request.data.get('user_id')
    gym_id = request.data.get('gym_id')
    entry_source = request.data.get('entry_source', 'QR_SCAN')

    if not member_id or not gym_id:
        return Response(
            {'error': 'user_id and gym_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)
    member = get_object_or_404(GymMember, pk=member_id, gym=gym)

    try:
        with transaction.atomic():
            attendance = GymAttendance.objects.create(
                gym=gym,
                member=member,
                entry_source=entry_source
            )
    except IntegrityError:
        return Response(
            {'error': 'Member already checked in today'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = GymAttendanceSerializer(attendance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def attendance_today(request, gym_id):
    gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)
    today = timezone.now().date()

    attendances = GymAttendance.objects.filter(
        gym=gym,
        date=today
    ).select_related('member', 'gym').order_by('-checkin_time')

    serializer = GymAttendanceSerializer(attendances, many=True)
    return Response(
        {'count': attendances.count(), 'results': serializer.data},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def attendance_stats(request, gym_id):
    gym = get_object_or_404(Gym, pk=gym_id, owner=request.user)
    days = int(request.query_params.get('days', 7))
    date_from = timezone.now().date() - timedelta(days=days)

    queryset = GymAttendance.objects.filter(
        gym=gym,
        date__gte=date_from
    )

    daily_breakdown = queryset.values('date').annotate(
        checkins=Count('id')
    ).order_by('-date')

    return Response({
        'total_checkins': queryset.count(),
        'unique_members': queryset.values('member').distinct().count(),
        'checkins_by_source': list(
            queryset.values('entry_source').annotate(count=Count('id'))
        ),
        'daily_breakdown': list(daily_breakdown)
    }, status=status.HTTP_200_OK)
