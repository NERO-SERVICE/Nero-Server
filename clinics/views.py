from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DrfClinics, DrfDrug, DrfDrugArchive
from .serializers import DrfClinicsSerializer, DrfDrugSerializer, DrfDrugArchiveSerializer
from django.utils import timezone
from django.db import transaction
from pytz import timezone as pytz_timezone

class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        # 요청 데이터 확인 로그 출력
        print("Request Data:", request.data)

        serializer = DrfClinicsSerializer(data=request.data)
        if serializer.is_valid():
            clinic = serializer.save(owner=request.user)
            
            # 약물 데이터를 처리하는 부분
            drugs_data = request.data.get('drugs', [])
            for drug_data in drugs_data:
                drug_archive_id = drug_data.get('drugArchive')
                drug_archive = get_object_or_404(DrfDrugArchive, id=drug_archive_id)
                
                DrfDrug.objects.create(
                    clinic=clinic, 
                    drugArchive=drug_archive, 
                    number=drug_data.get('number'), 
                    initialNumber=drug_data.get('initialNumber'), 
                    time=drug_data.get('time'), 
                    allow=drug_data.get('allow')
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 유효성 검사 실패 로그 출력
        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 클리닉 수정
class UpdateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)
        serializer = DrfClinicsSerializer(clinic, data=request.data, partial=True)

        if serializer.is_valid():
            clinic = serializer.save()

            # 기존 약물 삭제 후 새롭게 추가
            DrfDrug.objects.filter(clinic=clinic).delete()

            for drug_data in request.data.get('drugs', []):
                drug_archive_id = drug_data.pop('drugArchive')
                drug_archive = get_object_or_404(DrfDrugArchive, id=drug_archive_id)
                DrfDrug.objects.create(clinic=clinic, drugArchive=drug_archive, **drug_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        clinics = DrfClinics.objects.filter(owner=request.user).prefetch_related('drugs')
        
        if not clinics.exists():
            return Response({'detail': 'No clinics found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DrfClinicsSerializer(clinics, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# 약물 소비
class ConsumeSelectedDrugsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        drug_ids = request.data.get('drug_ids', [])
        if not drug_ids:
            return Response({'error': 'No drug IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        korea_time = now.astimezone(pytz_timezone('Asia/Seoul'))  # 한국 시간으로 변환
        today_start = korea_time.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timezone.timedelta(days=1)
        
        if korea_time >= tomorrow_start:
            drugs_to_reset = DrfDrug.objects.filter(clinic__owner=request.user, allow=False)
            for drug in drugs_to_reset:
                drug.reset_allow()
        
        consumed_drugs = []

        for drug_id in drug_ids:
            drug = get_object_or_404(DrfDrug, drugId=drug_id, clinic__owner=request.user)
            
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

# 특정 클리닉에 속한 약물 리스트 조회
class ListDrugsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)
        drugs = DrfDrug.objects.filter(clinic=clinic).select_related('drugArchive')
        serializer = DrfDrugSerializer(drugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# DrfDrugArchive 리스트 조회
class ListDrugArchivesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        drug_archives = DrfDrugArchive.objects.all()
        serializer = DrfDrugArchiveSerializer(drug_archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
