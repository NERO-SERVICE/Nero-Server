from rest_framework import serializers
from .models import DrfClinics, DrfDrug, DrfDrugArchive

class DrfDrugArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrugArchive
        fields = ['id', 'drugName', 'target', 'capacity']

class DrfDrugSerializer(serializers.ModelSerializer):
    drugArchive = DrfDrugArchiveSerializer()  # 중첩된 직렬화

    class Meta:
        model = DrfDrug
        fields = ['drugId', 'drugArchive', 'number', 'initialNumber', 'time', 'allow']

class DrfClinicsSerializer(serializers.ModelSerializer):
    drugs = DrfDrugSerializer(many=True)  # 중첩된 직렬화
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'nickname', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'description', 'drugs', 'clinicLatitude', 'clinicLongitude', 'locationLabel']

    def get_nickname(self, obj):
        return obj.owner.nickname

    # create 메서드 명시적 구현
    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')  # drugs 데이터 분리
        clinic = DrfClinics.objects.create(**validated_data)  # 클리닉 생성

        for drug_data in drugs_data:
            drug_archive_data = drug_data.pop('drugArchive')  # drugArchive 데이터 분리
            drug_archive = DrfDrugArchive.objects.get(id=drug_archive_data['id'])  # 존재하는 drugArchive 가져오기
            DrfDrug.objects.create(item=clinic, drugArchive=drug_archive, **drug_data)  # drug 생성

        return clinic
