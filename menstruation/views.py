from rest_framework import generics, permissions
from .models import Menstruation
from .serializers import MenstruationSerializer

class MenstruationListCreateView(generics.ListCreateAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Menstruation.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MenstruationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Menstruation.objects.filter(owner=self.request.user)
