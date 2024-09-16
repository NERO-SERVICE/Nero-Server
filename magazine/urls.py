from django.urls import path
from .views import ListMagazineView, CreateMagazineView, RetrieveMagazineView, UpdateMagazineView, DeleteMagazineView

app_name = "magazine"

urlpatterns = [
    path('', ListMagazineView.as_view(), name='list_magazines'),
    path('create/', CreateMagazineView.as_view(), name='create_magazine'),
    path('<int:id>/', RetrieveMagazineView.as_view(), name='get_magazine'),
    path('<int:id>/update/', UpdateMagazineView.as_view(), name='update_magazine'),
    path('<int:id>/delete/', DeleteMagazineView.as_view(), name='delete_magazine'),
]
