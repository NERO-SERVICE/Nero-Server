from rest_framework import serializers
from .models import Today
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'nickname', 'age', 'sex', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            age=validated_data['age'],
            sex=validated_data['sex']
        )
        return user

class TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Today
        fields = ('id', 'userId', 'date')