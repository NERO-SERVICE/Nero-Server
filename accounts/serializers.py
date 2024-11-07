from rest_framework import serializers
from .models import User, ProfileImage, Memories

class UserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='id', read_only=True)
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True)

    class Meta:
        model = User
        fields = [
            'userId', 'kakaoId', 'appleId', 'createdAt', 'nickname',
            'email', 'birth', 'sex', 'deletedAt'
        ]
        read_only_fields = ['userId', 'deletedAt']

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

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'birth', 'sex', 'profile_image']

    def update(self, instance, validated_data):
        profile_image_data = validated_data.pop('profile_image', None)

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create ProfileImage
        if profile_image_data:
            profile_image_instance, created = ProfileImage.objects.get_or_create(user=instance)
            if 'image' in profile_image_data:
                profile_image_instance.image = profile_image_data['image']
                profile_image_instance.save()
        return instance

class MemoriesSerializer(serializers.ModelSerializer):
    deletedAt = serializers.DateTimeField(source='deleted_at', read_only=True)

    class Meta:
        model = Memories
        fields = ['memoryId', 'userId', 'items', 'deletedAt']
        read_only_fields = ['memoryId', 'userId', 'deletedAt']