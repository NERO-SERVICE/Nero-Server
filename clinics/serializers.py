from rest_framework import serializers
from .models import DrfClinics, DrfDrug

class DrfDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrug
        fields = ['drugId', 'status', 'number', 'time', 'allow']

class DrfClinicsSerializer(serializers.ModelSerializer):
    drugs = DrfDrugSerializer(many=True)
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'drugs']
        
    def get_nickname(self, obj):
        return obj.owner.nickname

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs', [])
        clinic = DrfClinics.objects.create(**validated_data)
        for drug_data in drugs_data:
            DrfDrug.objects.create(item=clinic, **drug_data)
        return clinic

    def update(self, instance, validated_data):
        drugs_data = validated_data.pop('drugs', [])
        
        # 클리닉 기본 정보 업데이트
        instance.title = validated_data.get('title', instance.title)
        instance.recentDay = validated_data.get('recentDay', instance.recentDay)
        instance.nextDay = validated_data.get('nextDay', instance.nextDay)
        instance.save()

        # 기존 drugs 업데이트 또는 새로 추가
        existing_drug_ids = [drug.drugId for drug in instance.drugs.all()]
        new_drug_ids = [drug_data.get('drugId') for drug_data in drugs_data]

        # 업데이트 및 추가 로직
        for drug_data in drugs_data:
            drug_id = drug_data.get('drugId')
            if drug_id in existing_drug_ids:
                # 기존 약물 업데이트
                drug = DrfDrug.objects.get(drugId=drug_id, item=instance)
                drug.status = drug_data.get('status', drug.status)
                drug.number = drug_data.get('number', drug.number)
                drug.time = drug_data.get('time', drug.time)
                drug.save()
            else:
                # 새로운 약물 추가
                DrfDrug.objects.create(item=instance, **drug_data)

        # 삭제할 약물들
        for drug in instance.drugs.all():
            if drug.drugId not in new_drug_ids:
                drug.delete()

        return instance
