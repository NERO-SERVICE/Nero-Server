from django.urls import path
from .views import kakao_auth

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
]
