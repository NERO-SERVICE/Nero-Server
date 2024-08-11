from rest_framework import serializers
from .models import DrfProduct

class DrfProductSerializer(serializers.ModelSerializer):
    imageUrls = serializers.SerializerMethodField()

    class Meta:
        model = DrfProduct
        fields = [
            'id',
            'title',
            'description',
            'productPrice',
            'isFree',
            'imageUrls',
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