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

    drugArchives = serializers.PrimaryKeyRelatedField(queryset=DrfDrugArchive.objects.all(), many=True)

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'description', 'drugs', 'clinicLatitude', 'clinicLongitude', 'locationLabel', 'drugArchives']

    def get_nickname(self, obj):
        return obj.owner.nickname

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')
        drug_archives = validated_data.pop('drugArchives') 
        clinic = DrfClinics.objects.create(**validated_data)
        clinic.drugArchives.set(drug_archives)
        for drug_data in drugs_data:
            DrfDrug.objects.create(item=clinic, **drug_data)
        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', None)
        drug_archives = validated_data.pop('drugArchives', None)
        instance = super().update(instance, validated_data)
        
        if drug_archives:
            instance.drugArchives.set(drug_archives)
        if drugs_data:
            instance.drugs.all().delete()
            for drug_data in drugs_data:
                DrfDrug.objects.create(item=instance, **drug_data)
        return instance