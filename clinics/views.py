from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DrfClinics
from .serializers import DrfClinicsSerializer


# 제품 생성
class CreateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DrfClinicsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 제품 조회
class RetrieveClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clinicId):
        clinics = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)  # 유저가 소유한 제품인지 확인
        serializer = DrfClinicsSerializer(clinics, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# 제품 수정
class UpdateClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, clinicId):
        clinics = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)  # 유저가 소유한 제품인지 확인
        serializer = DrfClinicsSerializer(clinics, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 제품 삭제
class DeleteClinicView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, clinicId):
        clinics = get_object_or_404(DrfClinics, clinicId=clinicId, owner=request.user)  # 유저가 소유한 제품인지 확인
        clinics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 사용자가 소유한 모든 제품 리스트 조회
class ListClinicsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clinics = DrfClinics.objects.filter(owner=request.user)
        
        if not clinics.exists():
            return Response({'detail': 'No clinics found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DrfClinicsSerializer(clinics, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.drugs.all().delete()
        instance.delete()