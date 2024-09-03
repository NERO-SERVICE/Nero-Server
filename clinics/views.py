from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DrfClinics, DrfDrug, DrfDrugArchive
from .serializers import DrfClinicsSerializer, DrfDrugSerializer, DrfDrugArchiveSerializer
from django.utils import timezone

# 클리닉 생성
class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DrfClinicsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 클리닉 조회
class RetrieveClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)  # 유저가 소유한 클리닉인지 확인
        serializer = DrfClinicsSerializer(clinic, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# 클리닉 수정
class UpdateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)  # 유저가 소유한 클리닉인지 확인
        serializer = DrfClinicsSerializer(clinic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 클리닉 삭제
class DeleteClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, clinicId):
        clinic = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)  # 유저가 소유한 클리닉인지 확인
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
        
        # 자정을 지나면 약물의 allow 상태를 초기화
        if korea_time >= tomorrow_start:
            drugs_to_reset = DrfDrug.objects.filter(item__owner=request.user, allow=False)
            for drug in drugs_to_reset:
                drug.reset_allow()
        
        consumed_drugs = []

        for drug_id in drug_ids:
            drug = get_object_or_404(DrfDrug, drugId=drug_id, item__owner=request.user)
            
            # number가 0이면 소비할 수 없도록 방지
            if drug.number == 0:
                return Response({'error': f'Drug {drug.status} has run out and cannot be consumed.'}, status=status.HTTP_400_BAD_REQUEST)

            # allow가 False이면 소비할 수 없도록 방지
            if not drug.allow:
                return Response({'error': f'Drug {drug.status} has already been consumed today.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                drug.consume_one()
                drug.allow = False  # 약물이 소모되면 allow를 False로 설정
                drug.save()
                consumed_drugs.append({
                    'drugId': drug.drugId,
                    'status': drug.status,
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
    
    def get(self, request):
        drug_archives = DrfDrugArchive.objects.all()
        serializer = DrfDrugArchiveSerializer(drug_archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
