from rest_framework import generics, permissions
from .models import Mail
from .serializers import MailSerializer

class MailCreateView(generics.CreateAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
