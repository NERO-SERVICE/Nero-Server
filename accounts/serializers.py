from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'nickname', 'kakaoId', 'createdAt', 'updatedAt', 'temperature']

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'kakaoId', 'nickname', 'createdAt', 'updatedAt', 'temperature']
