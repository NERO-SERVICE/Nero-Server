from rest_framework import serializers
from .models import DrfProduct, ImageFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at']

class DrfProductSerializer(serializers.ModelSerializer):
    imageFiles = ImageFileSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = DrfProduct
        fields = [
            'id', 'title', 'description', 'productPrice', 'isFree',
            'imageFiles', 'uploaded_images', 'owner', 'createdAt', 'updatedAt',
            'viewCount', 'status', 'wantTradeLocation', 'wantTradeLocationLabel',
            'categoryType', 'likers'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = DrfProduct.objects.create(**validated_data)
        for image in uploaded_images:
            image_file = ImageFile.objects.create(file=image)
            product.imageFiles.add(image_file)
        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images:
            instance.imageFiles.clear() 
            for image in uploaded_images:
                image_file = ImageFile.objects.create(file=image)
                instance.imageFiles.add(image_file)

        return instance
