from django.urls import path, include
# from .views import UserCreateView
from .views import CustomRegisterView
app_name = 'accounts'

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
]