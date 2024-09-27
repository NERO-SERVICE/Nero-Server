from rest_framework import serializers
from .models import Information, InformationImageFile

class InformationImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationImageFile
        fields = ['file']

class InformationSerializer(serializers.ModelSerializer):
    imageUrls = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    imageFiles = InformationImageFileSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Information
        fields = [
            'infoId',
            'title',
            'description',
            'imageUrls',
            'imageFiles',
            'writer',
            'nickname',
            'createdAt',
            'updatedAt',
        ]

    def get_imageUrls(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.file.url) for image in obj.imageFiles.all()]

    def get_nickname(self, obj):
        return obj.writer.nickname

    def create(self, validated_data):
        image_files_data = self.initial_data.getlist('imageFiles')
        information = Information.objects.create(**validated_data)
        for image_data in image_files_data:
            InformationImageFile.objects.create(information=information, file=image_data)
        return information

    def update(self, instance, validated_data):
        image_files_data = validated_data.pop('imageFiles', None)
        information = super().update(instance, validated_data)
        if image_files_data is not None:
            instance.imageFiles.all().delete()
            for image_data in image_files_data:
                InformationImageFile.objects.create(information=information, **image_data)
        return information
