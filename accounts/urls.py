from django.urls import path
from .views import kakao_auth, userinfo, update_user_info, delete_account, MemoriesView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userinfo/', userinfo, name='userinfo'),
    path('update/', update_user_info, name='update_user_info'),
    path('delete/', delete_account, name='delete_account'),
    path('memories/', MemoriesView.as_view(), name='memories'),
]
