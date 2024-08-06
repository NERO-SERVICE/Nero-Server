from django.urls import path
from .views import kakao_auth, get_user_info

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
     path('userinfo/', get_user_info, name='get_user_info'),
]
