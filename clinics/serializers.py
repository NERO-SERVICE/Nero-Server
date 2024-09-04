from rest_framework import serializers
from .models import DrfClinics, DrfDrug, DrfDrugArchive

class DrfDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrugArchive
        fields = ['id', 'drugName', 'target', 'capacity']

class DrfDrugSerializer(serializers.ModelSerializer):
    drugArchive = serializers.PrimaryKeyRelatedField(queryset=DrfDrugArchive.objects.all())

    class Meta:
        model = DrfDrug
        fields = ['drugId', 'drugArchive', 'number', 'initialNumber', 'time', 'allow']

class DrfClinicsSerializer(serializers.ModelSerializer):
    drugs = DrfDrugSerializer(many=True) 
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'description', 'drugs', 'clinicLatitude', 'clinicLongitude', 'locationLabel']

    def get_nickname(self, obj):
        return obj.owner.nickname

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')
        clinic = DrfClinics.objects.create(**validated_data)
        for drug_data in drugs_data:
            DrfDrug.objects.create(item=clinic, **drug_data)
        return clinic

    
    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', None)
        instance = super().update(instance, validated_data)
        
        if drugs_data:
            # 기존 drugs 업데이트 또는 추가
            for drug_data in drugs_data:
                drug_id = drug_data.get('drugId', None)
                if drug_id:
                    # 기존 drug 업데이트
                    drug = DrfDrug.objects.get(drugId=drug_id, item=instance)
                    drug.number = drug_data.get('number', drug.number)
                    drug.initialNumber = drug_data.get('initialNumber', drug.initialNumber)
                    drug.time = drug_data.get('time', drug.time)
                    drug.allow = drug_data.get('allow', drug.allow)
                    drug.save()
                else:
                    # 새로운 drug 추가
                    DrfDrug.objects.create(item=instance, **drug_data)
        
        return instance
