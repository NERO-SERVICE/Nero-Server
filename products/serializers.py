# from rest_framework import serializers
# from .models import DrfProduct

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

from rest_framework import serializers
from .models import DrfProduct, ImageFile

class DrfProductSerializer(serializers.ModelSerializer):
    imageUrls = serializers.ListField(
        child=serializers.URLField(), write_only=True, required=False
    )
    imageUrls = serializers.SerializerMethodField(read_only=True)  # 서버에서 응답 시 사용할 필드

    class Meta:
        model = DrfProduct
        fields = [
            'id',
            'title',
            'description',
            'productPrice',
            'isFree',
            'imageUrls',  # 클라이언트와 서버 모두에서 'imageUrls' 사용
            'owner',
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

    def create(self, validated_data):
        image_urls = validated_data.pop('imageUrls', [])
        product = DrfProduct.objects.create(**validated_data)

        for url in image_urls:
            ImageFile.objects.create(product=product, file=url)

        return product
