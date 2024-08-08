from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'nickname', 'kakaoId', 'created_at', 'updated_at', 'temperature']

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'kakaoId', 'nickname', 'created_at', 'updated_at', 'temperature']
