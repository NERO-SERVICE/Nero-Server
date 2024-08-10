from django.urls import path
from .views import kakao_auth, login
from rest_framework_simplejwt.views import TokenRefreshView

app_name='accounts'

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
    path('login/', login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]