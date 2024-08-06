from django.urls import path
from .views import KakaoLogin, KakaoSignup, CheckNicknameView

urlpatterns = [
    path('social/login/', KakaoLogin.as_view(), name='kakao_login'),
    path('social/signup/', KakaoSignup.as_view(), name='kakao_signup'),
    path('check-nickname/', CheckNicknameView.as_view(), name='check_nickname'),
]