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
