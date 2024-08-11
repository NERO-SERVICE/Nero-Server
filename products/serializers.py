from rest_framework import serializers
from .models import DrfProduct, ImageFile

# class DrfProductSerializer(serializers.ModelSerializer):
#     imageUrls = serializers.SerializerMethodField()

#     class Meta:
#         model = DrfProduct
#         fields = [
#             'id',
#             'title',
#             'description',
#             'productPrice',
#             'isFree',
#             'imageUrls',
#             'owner',
#             'createdAt',
#             'updatedAt',
#             'viewCount',
#             'status',
#             'wantTradeLocation',
#             'wantTradeLocationLabel',
#             'categoryType',
#             'likers',
#         ]

#     def get_imageUrls(self, obj):
#         request = self.context.get('request')
#         return [request.build_absolute_uri(image.file.url) for image in obj.imageFiles.all()]

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['file']

class DrfProductSerializer(serializers.ModelSerializer):
    imageFiles = ImageFileSerializer(many=True, required=False)

    class Meta:
        model = DrfProduct
        fields = [
            'id', 'title', 'description', 'productPrice', 'isFree',
            'imageFiles', 'owner', 'createdAt', 'updatedAt', 'viewCount',
            'status', 'wantTradeLocation', 'wantTradeLocationLabel',
            'categoryType', 'likers'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('imageFiles', [])
        product = DrfProduct.objects.create(**validated_data)
        for image_data in images_data:
            ImageFile.objects.create(product=product, **image_data)
        return product
