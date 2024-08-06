from django.urls import path
from .views import KakaoLogin, KakaoSignup, CheckNicknameView, AddNickname

app_name='accounts'

urlpatterns = [
    path('signup/', KakaoSignup.as_view(), name='kakao_signup'),
    path('add-nickname/', AddNickname.as_view(), name='add_nickname'),
    path('login/', KakaoLogin.as_view(), name='kakao_login'),
    path('check-nickname/', CheckNicknameView.as_view(), name='check_nickname'),
]