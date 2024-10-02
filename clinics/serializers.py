from rest_framework import serializers
from .models import Clinics, Drug, DrugArchive, MyDrugArchive
from django.utils import timezone

class MyDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDrugArchive
        fields = ['myArchiveId', 'archiveId', 'drugName', 'target', 'capacity']
        read_only_fields = ['myArchiveId']

class DrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugArchive
        fields = ['archiveId', 'drugName', 'target', 'capacity']
        read_only_fields = ['archiveId']

class DrugSerializer(serializers.ModelSerializer):
    myDrugArchive = MyDrugArchiveSerializer()
    
    class Meta:
        model = Drug
        fields = ['drugId', 'myDrugArchive', 'number', 'initialNumber', 'time', 'allow']
        read_only_fields = ['drugId']


class ClinicsSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True)
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Clinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'description', 'drugs']
        read_only_fields = ['clinicId', 'owner', 'createdAt', 'updatedAt']

    def get_nickname(self, obj):
        return obj.owner.nickname

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')
        
        clinic = Clinics.objects.create(
            owner=self.context['request'].user,
            createdAt=timezone.now(),
            **validated_data
        )
    
        for drug_data in drugs_data:
            my_drug_archive_data = drug_data.pop('myDrugArchive')

            my_drug_archive = MyDrugArchive.objects.create(
                owner=clinic.owner,
                archiveId=my_drug_archive_data['archiveId'],
                drugName=my_drug_archive_data['drugName'],
                target=my_drug_archive_data.get('target', ''),
                capacity=my_drug_archive_data.get('capacity', '')
            )

            Drug.objects.create(
                clinic=clinic,
                myDrugArchive=my_drug_archive,
                number=drug_data.get('number', 0),
                initialNumber=drug_data.get('initialNumber', 0),
                time=drug_data.get('time', '아침'),
                allow=drug_data.get('allow', True)
            )

        return clinic