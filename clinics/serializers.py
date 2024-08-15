from rest_framework import serializers
from .models import DrfClinics, DrfDrug
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

class DrfDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrug
        fields = ['drugId', 'status', 'number', 'time']

class DrfClinicsSerializer(serializers.ModelSerializer):
    drugs = DrfDrugSerializer(many=True)

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'drugs']

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs', [])
        clinic = DrfClinics.objects.create(**validated_data)
        for drug_data in drugs_data:
            DrfDrug.objects.create(item=clinic, **drug_data)
        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', [])
        instance.title = validated_data.get('title', instance.title)
        instance.recentDay = validated_data.get('recentDay', instance.recentDay)
        instance.nextDay = validated_data.get('nextDay', instance.nextDay)
        instance.save()

        # 기존 drugs 삭제 후 재생성
        instance.drugs.all().delete()
        for drug_data in drugs_data:
            DrfDrug.objects.create(item=instance, **drug_data)

        return instance
