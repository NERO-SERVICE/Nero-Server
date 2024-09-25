from django.urls import path
from .views import MailCreateView

app_name = 'mail'

urlpatterns = [
    path('create/', MailCreateView.as_view(), name='mail-create'),
]
