from django.urls import path, include
# from .views import UserCreateView
from .views import CustomRegisterView, KakaoLogin
app_name = 'accounts'

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('api/social/', include('allauth.socialaccount.urls')),
    path('api/social/login/kakao/', KakaoLogin.as_view(), name='kakao_login'),
]