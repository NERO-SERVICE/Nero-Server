from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(max_length=255, source='id')
    
    class Meta:
        model = User
        fields = ['userId', 'kakaoId', 'createdAt', 'nickname', 'email', 'birth', 'sex']