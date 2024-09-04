from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DrfClinics, DrfDrug, DrfDrugArchive
from .serializers import DrfClinicsSerializer, DrfDrugSerializer, DrfDrugArchiveSerializer
from django.utils import timezone
from django.db import transaction

# 클리닉 생성
class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        clinic_data = request.data.copy()
        drugs_data = clinic_data.pop('drugs', [])
        
        clinic = DrfClinics.objects.create(owner=request.user, **clinic_data)
        
        for drug_data in drugs_data:
            drug_archive_id = drug_data.pop('drugArchive')
            drug_archive = get_object_or_404(DrfDrugArchive, id=drug_archive_id)
            DrfDrug.objects.create(item=clinic, drugArchive=drug_archive, **drug_data)
        
        serializer = DrfClinicsSerializer(clinic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 클리닉 수정
class UpdateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)
        clinic_data = request.data.copy()
        drugs_data = clinic_data.pop('drugs', [])
        
        # 클리닉 정보 업데이트
        for attr, value in clinic_data.items():
            setattr(clinic, attr, value)
        clinic.save()
        
        # 기존 약물 삭제 후 새롭게 추가
        DrfDrug.objects.filter(item=clinic).delete()
        
        for drug_data in drugs_data:
            drug_archive_id = drug_data.pop('drugArchive')
            drug_archive = get_object_or_404(DrfDrugArchive, id=drug_archive_id)
            DrfDrug.objects.create(item=clinic, drugArchive=drug_archive, **drug_data)
        
        serializer = DrfClinicsSerializer(clinic)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 특정 클리닉 조회
class RetrieveClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)
        serializer = DrfClinicsSerializer(clinic, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# 클리닉 삭제
class DeleteClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)
        clinic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 사용자가 소유한 모든 클리닉 리스트 조회
class ListClinicsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinics = DrfClinics.objects.filter(owner=request.user)
        
        if not clinics.exists():
            return Response({'detail': 'No clinics found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DrfClinicsSerializer(clinics, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConsumeSelectedDrugsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        drug_ids = request.data.get('drug_ids', [])
        if not drug_ids:
            return Response({'error': 'No drug IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        korea_time = now.astimezone(timezone.get_fixed_timezone(540))  # 한국 시간으로 변환 (UTC+9)
        today_start = korea_time.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timezone.timedelta(days=1)
        
        if korea_time >= tomorrow_start:
            drugs_to_reset = DrfDrug.objects.filter(item__owner=request.user, allow=False)
            for drug in drugs_to_reset:
                drug.reset_allow()
        
        consumed_drugs = []

        for drug_id in drug_ids:
            drug = get_object_or_404(DrfDrug, drugId=drug_id, item__owner=request.user)
            
            if drug.number == 0:
                return Response({'error': f'Drug {drug.drugArchive.drugName} has run out and cannot be consumed.'}, status=status.HTTP_400_BAD_REQUEST)

            if not drug.allow:
                return Response({'error': f'Drug {drug.drugArchive.drugName} has already been consumed today.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                drug.consume_one()
                drug.allow = False
                drug.save()
                consumed_drugs.append({
                    'drugId': drug.drugId,
                    'drugName': drug.drugArchive.drugName,
                    'number': drug.number,
                    'initialNumber': drug.initialNumber,
                    'time': drug.time,
                    'allow': drug.allow
                })
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'consumed_drugs': consumed_drugs}, status=status.HTTP_200_OK)

class ListDrugsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)
        drugs = DrfDrug.objects.filter(item=clinic)
        serializer = DrfDrugSerializer(drugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# DrfDrugArchive 리스트 조회
class ListDrugArchivesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        drug_archives = DrfDrugArchive.objects.all()
        serializer = DrfDrugArchiveSerializer(drug_archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
