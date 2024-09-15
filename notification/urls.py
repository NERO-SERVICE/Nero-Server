from django.urls import path
from .views import ListNoticeView, CreateNoticeView, RetrieveNoticeView, UpdateNoticeView, DeleteNoticeView

app_name = "notification"

urlpatterns = [
    path('', ListNoticeView.as_view(), name='list_notifications'),
    path('create/', CreateNoticeView.as_view(), name='create_notification'),
    path('<int:id>/', RetrieveNoticeView.as_view(), name='get_notification'),
    path('<int:id>/update/', UpdateNoticeView.as_view(), name='update_notification'),
    path('<int:id>/delete/', DeleteNoticeView.as_view(), name='delete_notification'),
]
