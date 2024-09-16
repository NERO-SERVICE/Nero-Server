from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Clinics, Drug, DrugArchive, MyDrugArchive
from .serializers import ClinicsSerializer, DrugSerializer, DrugArchiveSerializer
from django.utils import timezone
from django.db import transaction
from pytz import timezone as pytz_timezone

class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        print("Request Data:", request.data)
        serializer = ClinicsSerializer(data=request.data)

        if serializer.is_valid():
            clinic = serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, clinicId):
        clinic = get_object_or_404(Clinics, clinicId=clinicId, owner=request.user)
        serializer = ClinicsSerializer(clinic, data=request.data, partial=True)

        if serializer.is_valid():
            clinic = serializer.save()

            # 기존 약물 삭제 후 새롭게 추가
            Drug.objects.filter(clinic=clinic).delete()

            for drug_data in request.data.get('drugs', []):
                # MyDrugArchive를 생성하거나 수정
                my_drug_archive, created = MyDrugArchive.objects.get_or_create(
                    owner=clinic.owner,
                    archiveId=drug_data['myDrugArchive']['archiveId'],
                    defaults={
                        'drugName': drug_data['myDrugArchive']['drugName'],
                        'target': drug_data['myDrugArchive']['target'],
                        'capacity': drug_data['myDrugArchive']['capacity'],
                    }
                )
                
                # Drug 생성
                Drug.objects.create(
                    clinic=clinic,
                    myDrugArchive=my_drug_archive,
                    number=drug_data['number'],
                    initialNumber=drug_data['initialNumber'],
                    time=drug_data['time'],
                    allow=drug_data['allow']
                )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinicId):
        clinic = get_object_or_404(Clinics, clinicId=clinicId, owner=request.user)
        serializer = ClinicsSerializer(clinic, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, clinicId):
        clinic = get_object_or_404(Clinics, clinicId=clinicId, owner=request.user)
        clinic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListClinicsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinics = Clinics.objects.filter(owner=request.user).prefetch_related('drugs')
        
        if not clinics.exists():
            return Response({'detail': 'No clinics found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClinicsSerializer(clinics, many=True, context={'request': request})
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
            drugs_to_reset = Drug.objects.filter(clinic__owner=request.user, allow=False)
            for drug in drugs_to_reset:
                drug.reset_allow()
        
        consumed_drugs = []

        for drug_id in drug_ids:
            drug = get_object_or_404(Drug, drugId=drug_id, clinic__owner=request.user)
            
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
        clinic = get_object_or_404(Clinics, clinicId=clinicId, owner=request.user)
        drugs = Drug.objects.filter(clinic=clinic).select_related('myDrugArchive')
        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListDrugArchivesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        drug_archives = DrugArchive.objects.all()
        serializer = DrugArchiveSerializer(drug_archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RollbackConsumeDrugsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        date_to_rollback = request.data.get('date', None)
        
        if not date_to_rollback:
            return Response({'error': 'No date provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 입력된 날짜를 Python의 날짜 형식으로 변환
            rollback_date = timezone.datetime.strptime(date_to_rollback, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        korea_time = timezone.now().astimezone(pytz_timezone('Asia/Seoul')).date()

        # 롤백하려는 날짜가 오늘 이후인 경우 롤백 불가
        if rollback_date > korea_time:
            return Response({'error': 'Cannot rollback future dates.'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 날짜에 소비된 약물들 가져오기
        drugs_to_rollback = Drug.objects.filter(
            clinic__owner=request.user,
            allow=False,
            clinic__recentDay__date=rollback_date
        )

        if not drugs_to_rollback.exists():
            return Response({'detail': 'No consumed drugs found for the given date.'}, status=status.HTTP_404_NOT_FOUND)

        # 약물 소비 상태 롤백 (allow = True로 변경) 및 number 복구
        for drug in drugs_to_rollback:
            if drug.number < drug.initialNumber:
                drug.number += 1  # 이미 소비한 약물의 수량 복구
            drug.allow = True   # allow 상태를 롤백
            drug.save()

        return Response({'detail': f'Successfully rolled back drug consumption for {date_to_rollback}.'}, status=status.HTTP_200_OK)
