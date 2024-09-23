from rest_framework import generics
from rest_framework.views import APIView
from .models import Menstruation
from rest_framework.response import Response
from .serializers import MenstruationSerializer
from rest_framework.permissions import IsAuthenticated

class MenstruationListCreateView(generics.ListCreateAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menstruation.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MenstruationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menstruation.objects.filter(owner=self.request.user)

class MenstruationCycleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))

        cycles = Menstruation.objects.filter(
            owner=request.user,
            startDate__year__lte=year,
            endDate__year__gte=year,
            startDate__month__lte=month,
            endDate__month__gte=month,
        )

        serializer = MenstruationSerializer(cycles, many=True)
        return Response(serializer.data)