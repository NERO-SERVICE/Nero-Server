from rest_framework import serializers
from .models import DrfProduct

class DrfProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfProduct
        fields = '__all__'
