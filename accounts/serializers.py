from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(max_length=255, source='id')
    
    class Meta:
        model = User
        fields = ['uid', 'nickname', 'kakaoId', 'createdAt', 'updatedAt', 'temperature']

class UserSignUpSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(max_length=255, source='id')
    
    class Meta:
        model = User
        fields = ['uid', 'kakaoId', 'nickname', 'createdAt', 'updatedAt', 'temperature']
