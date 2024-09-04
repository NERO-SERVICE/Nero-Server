from rest_framework import serializers
from .models import DrfClinics, DrfDrug, DrfDrugArchive

class DrfDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrugArchive
        fields = ['id', 'drugName', 'target', 'capacity']

    def create(self, validated_data):
        # 중복된 drugName이 있는지 확인 후 없으면 새로 생성
        drug_archive, created = DrfDrugArchive.objects.get_or_create(
            drugName=validated_data['drugName'],
            defaults={'target': validated_data.get('target'), 'capacity': validated_data.get('capacity')}
        )
        return drug_archive

class DrfDrugSerializer(serializers.ModelSerializer):
    drugArchive = DrfDrugArchiveSerializer(many=True)

    class Meta:
        model = DrfDrug
        fields = ['drugId', 'drugArchive', 'number', 'initialNumber', 'time', 'allow']

    def create(self, validated_data):
        drug_archives_data = validated_data.pop('drugArchive')
        drug = DrfDrug.objects.create(**validated_data)
        for drug_archive_data in drug_archives_data:
            drug_archive = DrfDrugArchive.objects.get_or_create(
                id=drug_archive_data.get('id', None),
                defaults={
                    'drugName': drug_archive_data.get('drugName'),
                    'target': drug_archive_data.get('target'),
                    'capacity': drug_archive_data.get('capacity')
                }
            )[0]
            drug.drugArchive.add(drug_archive)
        return drug

    def update(self, instance, validated_data):
        drug_archives_data = validated_data.pop('drugArchive')
        instance.number = validated_data.get('number', instance.number)
        instance.time = validated_data.get('time', instance.time)
        instance.allow = validated_data.get('allow', instance.allow)
        instance.save()

        instance.drugArchive.clear()
        for drug_archive_data in drug_archives_data:
            drug_archive = DrfDrugArchive.objects.get_or_create(
                id=drug_archive_data.get('id', None),
                defaults={
                    'drugName': drug_archive_data.get('drugName'),
                    'target': drug_archive_data.get('target'),
                    'capacity': drug_archive_data.get('capacity')
                }
            )[0]
            instance.drugArchive.add(drug_archive)

        return instance

class DrfClinicsSerializer(serializers.ModelSerializer):
    drugs = DrfDrugSerializer(many=True)
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'description', 'drugs', 'clinicLatitude', 'clinicLongitude', 'locationLabel']

    def get_nickname(self, obj):
        return obj.owner.nickname

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs', [])
        clinic = DrfClinics.objects.create(**validated_data)
        for drug_data in drugs_data:
            drug_archives_data = drug_data.pop('drugArchive')
            drug = DrfDrug.objects.create(item=clinic, **drug_data)
            for drug_archive_data in drug_archives_data:
                drug_archive = DrfDrugArchive.objects.get_or_create(
                    id=drug_archive_data.get('id', None),
                    defaults={
                        'drugName': drug_archive_data.get('drugName'),
                        'target': drug_archive_data.get('target'),
                        'capacity': drug_archive_data.get('capacity')
                    }
                )[0]
                drug.drugArchive.add(drug_archive)
            drug.initialNumber = drug.number
            drug.save()
        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.recentDay = validated_data.get('recentDay', instance.recentDay)
        instance.nextDay = validated_data.get('nextDay', instance.nextDay)
        instance.clinicLatitude = validated_data.get('clinicLatitude', instance.clinicLatitude)
        instance.clinicLongitude = validated_data.get('clinicLongitude', instance.clinicLongitude)
        instance.locationLabel = validated_data.get('locationLabel', instance.locationLabel)
        instance.save()

        # 기존 drugs 업데이트 또는 새로 추가
        existing_drug_ids = [drug.drugId for drug in instance.drugs.all()]
        new_drug_ids = [drug_data.get('drugId') for drug_data in drugs_data]

        for drug_data in drugs_data:
            drug_id = drug_data.get('drugId')
            drug_archives_data = drug_data.pop('drugArchive')
            if drug_id in existing_drug_ids:
                drug = DrfDrug.objects.get(drugId=drug_id, item=instance)
                drug.drugArchive.clear()
                for drug_archive_data in drug_archives_data:
                    drug_archive = DrfDrugArchive.objects.get_or_create(
                        id=drug_archive_data.get('id', None),
                        defaults={
                            'drugName': drug_archive_data.get('drugName'),
                            'target': drug_archive_data.get('target'),
                            'capacity': drug_archive_data.get('capacity')
                        }
                    )[0]
                    drug.drugArchive.add(drug_archive)
                drug.number = drug_data.get('number', drug.number)
                drug.save()
            else:
                drug = DrfDrug.objects.create(item=instance, **drug_data)
                for drug_archive_data in drug_archives_data:
                    drug_archive = DrfDrugArchive.objects.get_or_create(
                        id=drug_archive_data.get('id', None),
                        defaults={
                            'drugName': drug_archive_data.get('drugName'),
                            'target': drug_archive_data.get('target'),
                            'capacity': drug_archive_data.get('capacity')
                        }
                    )[0]
                    drug.drugArchive.add(drug_archive)

        for drug in instance.drugs.all():
            if drug.drugId not in new_drug_ids:
                drug.delete()

        return instance
