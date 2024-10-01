from rest_framework import serializers
from .models import Notification, ImageFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['file']

class NotificationSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    image_files = ImageFileSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'description',
            'image_urls',
            'image_files',
            'writer',
            'nickname',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'writer', 'created_at', 'updated_at']

    def get_image_urls(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.file.url) for image in obj.image_files.all()]

    def get_nickname(self, obj):
        return obj.writer.nickname

    def create(self, validated_data):
        image_files_data = self.initial_data.getlist('imageFiles')
        notification = Notification.objects.create(**validated_data)
        
        for image_data in image_files_data:
            ImageFile.objects.create(notification=notification, file=image_data)

        return notification

    def update(self, instance, validated_data):
        image_files_data = validated_data.pop('image_files', None)
        
        notification = super().update(instance, validated_data)

        if image_files_data is not None:
            instance.image_files.all().delete()
            for image_data in image_files_data:
                ImageFile.objects.create(notification=notification, **image_data)

        return notification
