from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Clinics, Drug, DrugArchive, MyDrugArchive
from mypage.models import YearlyLog
from .serializers import ClinicsSerializer, DrugSerializer, DrugArchiveSerializer
from django.utils import timezone
from django.db import transaction
from pytz import timezone as pytz_timezone

class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        print("Request Data:", request.data)
        serializer = ClinicsSerializer(data=request.data, context={'request': request})
    
        if serializer.is_valid():
            clinic = serializer.save()
            return Response(ClinicsSerializer(clinic, context={'request': request}).data, status=status.HTTP_201_CREATED)
    
        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, clinicId):
        clinic = get_object_or_404(Clinics, clinicId=clinicId, owner=request.user)
        serializer = ClinicsSerializer(clinic, data=request.data, partial=True, context={'request': request})
    
        if serializer.is_valid():
            clinic = serializer.save()
    
            # 기존 약물 삭제 후 새롭게 추가
            Drug.objects.filter(clinic=clinic).delete()
    
            for drug_data in request.data.get('drugs', []):
                # MyDrugArchive를 생성하거나 수정
                my_drug_archive_data = drug_data.get('myDrugArchive', {})
                my_drug_archive, created = MyDrugArchive.objects.get_or_create(
                    owner=clinic.owner,
                    archiveId=my_drug_archive_data['archiveId'],
                    defaults={
                        'drugName': my_drug_archive_data.get('drugName', ''),
                        'target': my_drug_archive_data.get('target', ''),
                        'capacity': my_drug_archive_data.get('capacity', ''),
                    }
                )
                
                # Drug 생성
                Drug.objects.create(
                    clinic=clinic,
                    myDrugArchive=my_drug_archive,
                    number=drug_data.get('number', 0),
                    initialNumber=drug_data.get('initialNumber', 0),
                    time=drug_data.get('time', '아침'),
                    allow=drug_data.get('allow', True)
                )
    
            return Response(ClinicsSerializer(clinic, context={'request': request}).data, status=status.HTTP_200_OK)
    
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

    @transaction.atomic
    def post(self, request):
        drug_ids = request.data.get('drug_ids', [])
        if not drug_ids:
            return Response({'error': 'No drug IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        korea_time = now.astimezone(pytz_timezone('Asia/Seoul'))  # 한국 시간으로 변환
        today_date = korea_time.date()
        
        # 오늘 복용해야 하는 모든 약물
        today_drugs = Drug.objects.filter(
            clinic__owner=request.user, 
            allow=True, 
            clinic__recentDay__date=today_date
        )
        
        # 오늘 복용한 약물을 처리
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

        # 오늘 복용해야 하는 모든 약물이 allow=False 상태인지 확인하고 기록
        if Drug.objects.filter(clinic__owner=request.user, clinic__recentDay__date=today_date, allow=True).count() == 0:
            YearlyLog.objects.get_or_create(
                owner=request.user,
                date=today_date,
                log_type='dose',
                defaults={'action': True}
            )

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

    @transaction.atomic
    def post(self, request):
        date_to_rollback = request.data.get('date', None)
        
        if not date_to_rollback:
            return Response({'error': 'No date provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rollback_date = timezone.datetime.strptime(date_to_rollback, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        korea_time = timezone.now().astimezone(pytz_timezone('Asia/Seoul')).date()

        # 롤백하려는 날짜가 오늘 이후인 경우 롤백 불가
        if rollback_date > korea_time:
            return Response({'error': 'Cannot rollback future dates.'}, status=status.HTTP_400_BAD_REQUEST)

        # 로그인한 유저의 약물들만 롤백
        drugs_to_rollback = Drug.objects.filter(
            clinic__owner=request.user,  # 유저 필터링
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

        # YearlyLog 롤백 처리
        try:
            yearly_log = YearlyLog.objects.get(
                owner=request.user,  # 유저 필터링
                date=rollback_date,
                log_type='dose'
            )
            yearly_log.action = False
            yearly_log.save()
        except YearlyLog.DoesNotExist:
            pass

        return Response({'detail': f'Successfully rolled back drug consumption for {date_to_rollback}.'}, status=status.HTTP_200_OK)
