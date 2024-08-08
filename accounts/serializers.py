from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'nickname', 'kakao_id', 'created_at', 'updated_at', 'temperature']

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'kakao_id', 'nickname', 'created_at', 'updated_at', 'temperature']
