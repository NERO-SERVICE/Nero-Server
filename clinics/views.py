from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import DrfClinics, DrfDrug
from .serializers import DrfClinicsSerializer, DrfDrugSerializer

class ListClinicsView(generics.ListCreateAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DrfClinics.objects.filter(owner=self.request.user)
        
class CreateClinicView(generics.CreateAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RetrieveClinicView(generics.RetrieveAPIView):
    serializer_class = DrfClinicsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clinic_id = self.kwargs.get('clinicId')
        try:
            return DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")

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

class ListDrugsView(generics.ListCreateAPIView):
    serializer_class = DrfDrugSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = self.kwargs.get('clinicId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
            return DrfDrug.objects.filter(item=clinic)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")
        
class CreateDrugView(generics.CreateAPIView):
    serializer_class = DrfDrugSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        clinic_id = self.kwargs.get('clinicId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
            serializer.save(item=clinic)
        except DrfClinics.DoesNotExist:
            raise NotFound("Clinic not found or you do not have permission to access it.")
        
class RetrieveDrugView(generics.RetrieveAPIView):
    serializer_class = DrfDrugSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clinic_id = self.kwargs.get('clinicId')
        drug_id = self.kwargs.get('drugId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
            return DrfDrug.objects.get(drugId=drug_id, item=clinic)
        except (DrfClinics.DoesNotExist, DrfDrug.DoesNotExist):
            raise NotFound("Drug or Clinic not found or you do not have permission to access it.")

class UpdateDrugView(generics.UpdateAPIView):
    serializer_class = DrfDrugSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clinic_id = self.kwargs.get('clinicId')
        drug_id = self.kwargs.get('drugId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
            return DrfDrug.objects.get(drugId=drug_id, item=clinic)
        except (DrfClinics.DoesNotExist, DrfDrug.DoesNotExist):
            raise NotFound("Drug or Clinic not found or you do not have permission to access it.")

class DeleteDrugView(generics.DestroyAPIView):
    serializer_class = DrfDrugSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clinic_id = self.kwargs.get('clinicId')
        drug_id = self.kwargs.get('drugId')
        try:
            clinic = DrfClinics.objects.get(clinicId=clinic_id, owner=self.request.user)
            return DrfDrug.objects.get(drugId=drug_id, item=clinic)
        except (DrfClinics.DoesNotExist, DrfDrug.DoesNotExist):
            raise NotFound("Drug or Clinic not found or you do not have permission to access it.")
