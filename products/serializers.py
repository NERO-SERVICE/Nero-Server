from rest_framework import serializers
from .models import DrfProduct
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

class DrfProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
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