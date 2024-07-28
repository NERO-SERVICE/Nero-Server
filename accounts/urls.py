from django.urls import path, include
from .views import UserCreateView

app_name = 'accounts'

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('signup/', UserCreateView.as_view(), name='signup'),
]