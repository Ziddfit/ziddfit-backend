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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, gym_id, transaction_id):
    try:
        transaction = get_object_or_404(Transaction, gym=gym_id, id=transaction_id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'retrieval failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transaction_reverse(request, gym_id, transaction_id):
    try:
        original = get_object_or_404(Transaction, gym_id = gym_id, id =  transaction_id)

        if original.is_reversal:
            return Response({ 'message' :'cannot reverse a reversal transaction'}, status = status.HTTP_400_BAD_REQUEST)    
        if Transaction.objects.filter(reversal_of=original).exists():
           return Response({ 'message' : 'the transaction is already reversed'}, status = status.HTTP_400_BAD_REQUEST)
        
        reversal = Transaction.objects.create(
            gym = original.gym,
            amount = original.amount,
            category = original.category,
            party_name = original.party_name,
            party_type = original.party_type,
            member = original.member,
            staff = original.staff,

            transaction_type = 'credit' if original.transaction_type == 'debit' else 'debit',
            name = f"reversal - {original.name}",
            is_reversal = True,
            reversal_of = original,

            metadata = original.metadata
        )

        serializer = TransactionSerializer(reversal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': 'reversal failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)