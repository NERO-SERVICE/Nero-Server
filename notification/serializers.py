from rest_framework import serializers
from .models import Notification, ImageFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['file']

class NotificationSerializer(serializers.ModelSerializer):
    imageUrls = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    imageFiles = ImageFileSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'description',
            'imageUrls',
            'imageFiles',
            'writer',
            'nickname',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'writer', 'created_at', 'updated_at']
        
    def get_imageUrls(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.file.url) for image in obj.imageFiles.all()]

    def get_nickname(self, obj):
        return obj.writer.nickname

    def create(self, validated_data):
        image_files_data = self.initial_data.getlist('imageFiles')
        notification = Notification.objects.create(**validated_data)
        
        for image_data in image_files_data:
            ImageFile.objects.create(notification=notification, file=image_data)

        return notification

    def update(self, instance, validated_data):
        image_files_data = validated_data.pop('imageFiles', None)
        
        notification = super().update(instance, validated_data)

        if image_files_data is not None:
            instance.imageFiles.all().delete()
            for image_data in image_files_data:
                ImageFile.objects.create(notification=notification, **image_data)

        return notification
