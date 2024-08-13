from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import DrfClinics
from .serializers import DrfClinicsSerializer

class ListClinicsView(generics.ListAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DrfClinics.objects.filter(owner=self.request.user)

class CreateClinicView(generics.CreateAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpdateClinicView(generics.UpdateAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clinic_id = self.kwargs.get('clinicId')
        try:
            return DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")

class DeleteClinicView(generics.DestroyAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clinic_id = self.kwargs.get('clinicId')
        try:
            return DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")

    def perform_destroy(self, instance):
        # 이 클리닉에 속한 모든 drugs도 함께 삭제합니다.
        instance.drugs.all().delete()
        instance.delete()
