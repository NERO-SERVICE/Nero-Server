from django.urls import path
from .views import kakao_auth, login, userinfo, update_user_info, MemoriesView
from rest_framework_simplejwt.views import TokenRefreshView

app_name='accounts'

urlpatterns = [
    path('auth/kakao/', kakao_auth, name='kakao_auth'),
    path('login/', login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userinfo/', userinfo, name='userinfo'),
    path('update/', update_user_info, name='update_user_info'),
    path('memories/', MemoriesView.as_view(), name='memories'),
]