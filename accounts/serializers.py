from rest_framework import serializers
from .models import User, Memories

class UserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(max_length=255, source='id')
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True) 
    profile_image = serializers.ImageField(required=False, allow_null=True)
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'userId', 'kakaoId', 'appleId', 'createdAt', 'nickname',
            'email', 'birth', 'sex', 'deletedAt', 'profile_image', 'profile_image_url'
        ]
        read_only_fields = ['userId', 'deletedAt', 'profile_image_url']
        
    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return request.build_absolute_uri(obj.profile_image.url)
        return None

class MemoriesSerializer(serializers.ModelSerializer):
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True)

    class Meta:
        model = Memories
        fields = ['memoryId', 'userId', 'items', 'deletedAt']
        read_only_fields = ['memoryId', 'userId', 'deletedAt']
        
class UserProfileUpdateInfoSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'birth', 'sex', 'profile_image']