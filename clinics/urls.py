from django.urls import path
from .views import (
    ListClinicsView,
    CreateClinicView,
    RetrieveClinicView,
    UpdateClinicView,
    DeleteClinicView,
    ListDrugsView,
    ConsumeSelectedDrugsView,
    ListDrugArchivesView,
)

app_name = "clinics"

urlpatterns = [
    path('lists/', ListClinicsView.as_view(), name='list_clinics'),
    path('create/', CreateClinicView.as_view(), name='create_clinic'),
    path('<int:clinicId>/', RetrieveClinicView.as_view(), name='retrieve_clinic'),
    path('<int:clinicId>/update/', UpdateClinicView.as_view(), name='update_clinic'),
    path('<int:clinicId>/delete/', DeleteClinicView.as_view(), name='delete_clinic'),
    path('<int:clinicId>/drugs/', ListDrugsView.as_view(), name='list_drugs'),
    path('drugs/consume/', ConsumeSelectedDrugsView.as_view(), name='consume_selected_drugs'), 
    path('drugs/archives/', ListDrugArchivesView.as_view(), name='list_drug_archives'),
]