from django.urls import path
from .views import UserCreateView

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
]