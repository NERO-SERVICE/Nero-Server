from rest_framework import serializers
from .models import Clinics, Drug, DrugArchive, MyDrugArchive

class DrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugArchive
        fields = ['archiveId', 'drugName', 'target', 'capacity']


class MyDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDrugArchive
        fields = ['myArchiveId', 'archiveId', 'drugName', 'target', 'capacity']


class DrugSerializer(serializers.ModelSerializer):
    myDrugArchive = MyDrugArchiveSerializer()

    class Meta:
        model = Drug
        fields = ['drugId', 'myDrugArchive', 'number', 'initialNumber', 'time', 'allow']


class ClinicsSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True)
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Clinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'description', 'drugs']

    def get_nickname(self, obj):
        return obj.owner.nickname

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')
        clinic = Clinics.objects.create(**validated_data)

        for drug_data in drugs_data:
            my_drug_archive_data = drug_data.pop('myDrugArchive')

            # MyDrugArchive 객체 생성
            my_drug_archive = MyDrugArchive.objects.create(
                owner=clinic.owner,
                archiveId=my_drug_archive_data['archiveId'],
                drugName=my_drug_archive_data['drugName'],
                target=my_drug_archive_data['target'],
                capacity=my_drug_archive_data['capacity']
            )

            # Drug 객체 생성
            Drug.objects.create(
                clinic=clinic,
                myDrugArchive=my_drug_archive,
                number=drug_data['number'],
                initialNumber=drug_data['initialNumber'],
                time=drug_data['time'],
                allow=drug_data['allow']
            )

        return clinic
