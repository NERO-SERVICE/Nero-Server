from rest_framework import serializers
from .models import DrfProduct

class DrfProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrfProduct
        fields = ['docId', 'title', 'description', 'productPrice', 'isFree', 'imageUrls', 'owner', 'createdAt', 'updatedAt', 'viewCount', 'status', 'wantTradeLocation', 'wantTradeLocationLabel', 'categoryType', 'likers']
