from rest_framework import serializers
from .models import Clinics, Drug, DrugArchive, MyDrugArchive

# DrugArchiveSerializer: 약물 아카이브 정보를 시리얼라이즈
class DrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugArchive
        fields = ['archiveId', 'drugName', 'target', 'capacity']
        read_only_fields = ['archiveId']


# MyDrugArchiveSerializer: 개별 사용자의 약물 정보 시리얼라이즈
class MyDrugArchiveSerializer(serializers.ModelSerializer):
    archiveId = serializers.IntegerField(source='archive.archiveId', read_only=True)
    drugName = serializers.CharField(source='archive.drugName', read_only=True)
    target = serializers.CharField(source='archive.target', allow_null=True, read_only=True)
    capacity = serializers.CharField(source='archive.capacity', allow_null=True, read_only=True)

    class Meta:
        model = MyDrugArchive
        fields = ['myArchiveId', 'archiveId', 'drugName', 'target', 'capacity']
        read_only_fields = ['myArchiveId']


# DrugSerializer: 진료 기록에 연결된 약물 정보 시리얼라이즈
class DrugSerializer(serializers.ModelSerializer):
    myDrugArchive = MyDrugArchiveSerializer()

    class Meta:
        model = Drug
        fields = ['drugId', 'myDrugArchive', 'number', 'initialNumber', 'time', 'allow']
        read_only_fields = ['drugId']


# ClinicsSerializer: 진료 기록을 시리얼라이즈
class ClinicsSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True, read_only=True)
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
            archive = DrugArchive.objects.get(archiveId=my_drug_archive_data['archiveId'])

            # MyDrugArchive 객체 생성 또는 가져오기
            my_drug_archive, created = MyDrugArchive.objects.get_or_create(
                owner=clinic.owner,
                archive=archive
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
                archive = DrugArchive.objects.get(archiveId=my_drug_archive_data['archiveId'])

                # MyDrugArchive 객체 생성 또는 가져오기
                my_drug_archive, created = MyDrugArchive.objects.get_or_create(
                    owner=instance.owner,
                    archive=archive
                )

                # Drug 객체 생성
                Drug.objects.create(
                    clinic=instance,
                    myDrugArchive=my_drug_archive,
                    number=drug_data.get('number', 0),
                    initialNumber=drug_data.get('initialNumber', 0),
                    time=drug_data.get('time', '아침'),
                    allow=drug_data.get('allow', True)
                )
        return instance
