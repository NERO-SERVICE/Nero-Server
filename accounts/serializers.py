from rest_framework import serializers
from .models import User, Memories

class UserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(max_length=255, source='id')
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True) 

    class Meta:
        model = User
        fields = ['userId', 'kakaoId', 'appleId', 'createdAt', 'nickname', 'email', 'birth', 'sex', 'deletedAt']
        read_only_fields = ['userId', 'deletedAt']

class MemoriesSerializer(serializers.ModelSerializer):
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True)

    class Meta:
        model = Memories
        fields = ['memoryId', 'userId', 'items', 'deletedAt']
        read_only_fields = ['memoryId', 'userId', 'deletedAt']

class MypageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname']