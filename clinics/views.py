from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DrfClinics, DrfDrug, DrfDrugArchive, DrfMyDrugArchive
from .serializers import DrfClinicsSerializer, DrfDrugSerializer, DrfDrugArchiveSerializer
from django.utils import timezone
from django.db import transaction
from pytz import timezone as pytz_timezone

class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        print("Request Data:", request.data)
        serializer = DrfClinicsSerializer(data=request.data)

        if serializer.is_valid():
            clinic = serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                # DrfMyDrugArchive를 생성하거나 수정
                my_drug_archive, created = DrfMyDrugArchive.objects.get_or_create(
                    owner=clinic.owner,
                    archiveId=drug_data['myDrugArchive']['archiveId'],
                    defaults={
                        'drugName': drug_data['myDrugArchive']['drugName'],
                        'target': drug_data['myDrugArchive']['target'],
                        'capacity': drug_data['myDrugArchive']['capacity'],
                    }
                )
                
                # DrfDrug 생성
                DrfDrug.objects.create(
                    clinic=clinic,
                    myDrugArchive=my_drug_archive,
                    number=drug_data['number'],
                    initialNumber=drug_data['initialNumber'],
                    time=drug_data['time'],
                    allow=drug_data['allow']
                )

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
                return Response({'error': f'Drug {drug.myDrugArchive.drugName} has run out and cannot be consumed.'}, status=status.HTTP_400_BAD_REQUEST)

            if not drug.allow:
                return Response({'error': f'Drug {drug.myDrugArchive.drugName} has already been consumed today.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                drug.consume_one()
                drug.allow = False
                drug.save()
                consumed_drugs.append({
                    'drugId': drug.drugId,
                    'drugName': drug.myDrugArchive.drugName,
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
        drugs = DrfDrug.objects.filter(clinic=clinic).select_related('myDrugArchive')
        serializer = DrfDrugSerializer(drugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# DrfDrugArchive 리스트 조회
class ListDrugArchivesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        drug_archives = DrfDrugArchive.objects.all()
        serializer = DrfDrugArchiveSerializer(drug_archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)