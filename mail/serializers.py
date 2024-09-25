from rest_framework import serializers
from .models import Mail

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = ['id', 'owner', 'created_at', 'suggestion']
        read_only_fields = ['id', 'owner', 'created_at']
