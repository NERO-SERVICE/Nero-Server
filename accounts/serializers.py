from rest_framework import serializers
from .models import User, Memories, ProfileImage

class ProfileImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProfileImage
        fields = ['image', 'image_url']
        read_only_fields = ['image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class UserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(max_length=255, source='id')
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True)
    profile_image = ProfileImageSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'userId', 'kakaoId', 'appleId', 'createdAt', 'nickname',
            'email', 'birth', 'sex', 'deletedAt', 'profile_image'
        ]
        read_only_fields = ['userId', 'deletedAt', 'profile_image']

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

    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_image:
            ProfileImage.objects.update_or_create(user=instance, defaults={'image': profile_image})
        return instance