from rest_framework import serializers
from .models import User, Memories

class UserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(max_length=255, source='id')
    
    class Meta:
        model = User
        fields = ['userId', 'kakaoId', 'createdAt', 'nickname', 'email', 'birth', 'sex']

class MemoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memories
        fields = ['memoryId', 'userId', 'items']
        read_only_fields = ['memoryId', 'userId']
