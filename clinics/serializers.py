from rest_framework import serializers
from .models import Clinics, Drug, DrugArchive, MyDrugArchive

class MyDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDrugArchive
        fields = ['myArchiveId', 'drug_archive', 'drugName', 'target', 'capacity']
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
        drugs_data = validated_data.pop('drugs', [])
        clinic = Clinics.objects.create(owner=self.context['request'].user, **validated_data)

        for drug_data in drugs_data:
            my_drug_archive_data = drug_data.pop('myDrugArchive')

            # `drug_archive` 키로 변경 (기존 'archiveId' 사용 부분 수정)
            my_drug_archive = MyDrugArchive.objects.create(
                owner=clinic.owner,
                drug_archive=DrugArchive.objects.get(pk=my_drug_archive_data['drug_archive']),
                drugName=my_drug_archive_data['drugName'],
                target=my_drug_archive_data.get('target', ''),
                capacity=my_drug_archive_data.get('capacity', '')
            )

            # Drug 객체 생성
            Drug.objects.create(
                clinic=clinic,
                myDrugArchive=my_drug_archive,
                number=drug_data.get('number', 0),
                initialNumber=drug_data.get('initialNumber', 0),
                time=drug_data.get('time', '아침'),
                allow=drug_data.get('allow', True)
            )

        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if drugs_data is not None:
            # 기존 약물 삭제 후 새롭게 추가
            Drug.objects.filter(clinic=instance).delete()
            for drug_data in drugs_data:
                my_drug_archive_data = drug_data.pop('myDrugArchive')
                my_drug_archive, created = MyDrugArchive.objects.get_or_create(
                    owner=instance.owner,
                    drug_archive=DrugArchive.objects.get(pk=my_drug_archive_data['drug_archive']),
                    defaults={
                        'drugName': my_drug_archive_data.get('drugName', ''),
                        'target': my_drug_archive_data.get('target', ''),
                        'capacity': my_drug_archive_data.get('capacity', ''),
                    }
                )
                Drug.objects.create(
                    clinic=instance,
                    myDrugArchive=my_drug_archive,
                    number=drug_data.get('number', 0),
                    initialNumber=drug_data.get('initialNumber', 0),
                    time=drug_data.get('time', '아침'),
                    allow=drug_data.get('allow', True)
                )
        return instance
