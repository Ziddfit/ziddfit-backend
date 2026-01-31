from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import GymMember, Gym
from ..serializers import MemberSerializer

@api_view(['GET', 'POST'])
def member_list(request):
    members = GymMember.objects.filter( Gym__owner = request.user)
    serializer = MemberSerializer(members, many=True)
    return serializer.data