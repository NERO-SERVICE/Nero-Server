from django.urls import path
from .views import kakao_auth, apple_auth, userinfo, update_user_info, delete_account, mypage_userinfo, MemoriesView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
    path('auth/apple/', apple_auth, name='apple_auth'),
    path('auth/apple/callback/', apple_auth, name='apple_auth_callback'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userinfo/', userinfo, name='userinfo'),
    path('mypage/userinfo/', mypage_userinfo, name='mypage_userinfo'),
    path('update/', update_user_info, name='update_user_info'),
    path('delete/', delete_account, name='delete_account'),
    path('memories/', MemoriesView.as_view(), name='memories'),
]
