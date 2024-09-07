from rest_framework import serializers
from .models import DrfClinics, DrfDrug, DrfDrugArchive, DrfMyDrugArchive

class DrfDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrugArchive
        fields = ['id', 'drugName', 'target', 'capacity']


class DrfMyDrugArchiveSerializer(serializers.ModelSerializer):
    drugArchive = DrfDrugArchiveSerializer()

    class Meta:
        model = DrfMyDrugArchive
        fields = ['id', 'drugArchive']


class DrfDrugSerializer(serializers.ModelSerializer):
    myDrugArchive = DrfMyDrugArchiveSerializer()

    class Meta:
        model = DrfDrug
        fields = ['drugId', 'myDrugArchive', 'number', 'initialNumber', 'time', 'allow']


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
            my_drug_archive_data = drug_data.pop('myDrugArchive')
            drug_archive_data = my_drug_archive_data.get('drugArchive')

            drug_archive = DrfDrugArchive.objects.get(id=drug_archive_data['id'])
            my_drug_archive = DrfMyDrugArchive.objects.create(owner=clinic.owner, drugArchive=drug_archive)
            DrfDrug.objects.create(clinic=clinic, myDrugArchive=my_drug_archive, **drug_data)
        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', None)
        instance = super().update(instance, validated_data)

        if drugs_data:
            instance.drugs.all().delete()
            for drug_data in drugs_data:
                my_drug_archive_data = drug_data.pop('myDrugArchive')
                drug_archive_data = my_drug_archive_data.get('drugArchive')

                drug_archive = DrfDrugArchive.objects.get(id=drug_archive_data['id'])
                my_drug_archive = DrfMyDrugArchive.objects.create(owner=instance.owner, drugArchive=drug_archive)
                DrfDrug.objects.create(clinic=instance, myDrugArchive=my_drug_archive, **drug_data)
        return instance
