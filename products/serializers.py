from rest_framework import serializers
from .models import DrfProduct, ImageFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['file']

class DrfProductSerializer(serializers.ModelSerializer):
    imageUrls = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    imageFiles = ImageFileSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = DrfProduct
        fields = [
            'id',
            'title',
            'description',
            'productPrice',
            'isFree',
            'imageUrls',
            'imageFiles',
            'owner',
            'nickname',
            'createdAt',
            'updatedAt',
            'viewCount',
            'status',
            'wantTradeLocation',
            'wantTradeLocationLabel',
            'categoryType',
            'likers',
        ]

    def get_imageUrls(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.file.url) for image in obj.imageFiles.all()]
    
    def get_nickname(self, obj):
        return obj.owner.nickname
    
    def create(self, validated_data):
        image_files_data = validated_data.pop('imageFiles', [])
        product = DrfProduct.objects.create(**validated_data)
        
        for image_data in image_files_data:
            ImageFile.objects.create(product=product, **image_data)
        
        return product

    def update(self, instance, validated_data):
        image_files_data = validated_data.pop('imageFiles', None)
        product = super().update(instance, validated_data)

        if image_files_data is not None:
            instance.imageFiles.all().delete() 
            for image_data in image_files_data:
                ImageFile.objects.create(product=product, **image_data)
        
        return product