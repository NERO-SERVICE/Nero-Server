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
            DrfDrug.objects.create(clinic=clinic, **drug_data)
        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', None)
        instance = super().update(instance, validated_data)
        
        if drugs_data:
            instance.drugs.all().delete()
            for drug_data in drugs_data:
                DrfDrug.objects.create(clinic=instance, **drug_data)
        return instance