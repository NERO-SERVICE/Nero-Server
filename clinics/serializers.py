from rest_framework import serializers
from .models import DrfClinics, DrfDrug, DrfDrugArchive, DrfMyDrugArchive

class DrfDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrugArchive
        fields = ['archiveId', 'drugName', 'target', 'capacity']


class DrfMyDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfMyDrugArchive
        fields = ['myArchiveId', 'archiveId', 'drugName', 'target', 'capacity']


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

            # DrfMyDrugArchive 객체 생성
            my_drug_archive = DrfMyDrugArchive.objects.create(
                owner=clinic.owner,
                archiveId=my_drug_archive_data['archiveId'],
                drugName=my_drug_archive_data['drugName'],
                target=my_drug_archive_data['target'],
                capacity=my_drug_archive_data['capacity']
            )

            # DrfDrug 객체 생성
            DrfDrug.objects.create(
                clinic=clinic,
                myDrugArchive=my_drug_archive,
                number=drug_data['number'],
                initialNumber=drug_data['initialNumber'],
                time=drug_data['time'],
                allow=drug_data['allow']
            )

        return clinic