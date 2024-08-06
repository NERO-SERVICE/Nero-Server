from django.urls import path
from .views import KakaoLogin

urlpatterns = [
    path('api/social/login/', KakaoLogin.as_view(), name='kakao_login'),
]