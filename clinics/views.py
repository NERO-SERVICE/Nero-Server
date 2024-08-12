from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated, NotFound
from .models import DrfClinics, DrfDrug
from .serializers import DrfClinicsSerializer, DrfDrugSerializer

class DrfClinicsViewSet(viewsets.ModelViewSet):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        
        return DrfClinics.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        serializer.save(owner=self.request.user)

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        clinic_id = self.kwargs.get('clinicId')
        try:
            return DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")

class DrfDrugViewSet(viewsets.ModelViewSet):
    serializer_class = DrfDrugSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        clinic_id = self.kwargs.get('clinicId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")
        return DrfDrug.objects.filter(item=clinic)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        clinic_id = self.kwargs.get('clinicId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")
        serializer.save(item=clinic)

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        clinic_id = self.kwargs.get('clinicId')
        drug_id = self.kwargs.get('drugId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
            return DrfDrug.objects.get(drugId=drug_id, item=clinic)
        except (DrfClinics.DoesNotExist, DrfDrug.DoesNotExist):
            raise NotFound("Drug or Clinic not found or you do not have permission to access it.")
