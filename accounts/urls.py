from django.urls import path
from .views import kakao_auth, get_user_info, check_nickname
app_name='accounts'

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
    path('userinfo/<str:uid>/', get_user_info, name='get_user_info'),
    path('check-nickname/', check_nickname, name='check_nickname'),
]