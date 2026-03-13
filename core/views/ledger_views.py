from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from core.models.ledger import Transaction
from core.serializers.transaction_serializer import TransactionSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list(request, gym_id):
    if request.method == 'GET':
        try:
            transactions = Transaction.objects.filter(gym=gym_id)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'retrieval failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(gym_id=gym_id, recorded_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'transaction creation failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
