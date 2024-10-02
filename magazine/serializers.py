from rest_framework import serializers
from .models import Magazine, MagazineImageFile

class MagazineImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineImageFile
        fields = ['file']

class MagazineSerializer(serializers.ModelSerializer):
    imageUrls = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    imageFiles = MagazineImageFileSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Magazine
        fields = [
            'magazineId',
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
        image_files_data = self.context['request'].FILES.getlist('imageFiles')
        magazine = Magazine.objects.create(**validated_data)
        self._save_image_files(magazine, image_files_data)
        return magazine

    def update(self, instance, validated_data):
        image_files_data = self.context['request'].FILES.getlist('imageFiles')
        magazine = super().update(instance, validated_data)
        if image_files_data:
            instance.imageFiles.all().delete()
            self._save_image_files(magazine, image_files_data)
        return magazine

    def _save_image_files(self, magazine, image_files_data):
        for image_data in image_files_data:
            MagazineImageFile.objects.create(magazine=magazine, file=image_data)
