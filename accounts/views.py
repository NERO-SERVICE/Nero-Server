from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests
from .serializers import CustomUserSerializer

User = get_user_model()

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter

    def post(self, request, *args, **kwargs):
        token = request.data.get('kakaoUid')
        # 검증된 토큰을 사용하여 사용자를 인증 및 등록합니다.
        # 토큰 검증 로직을 구현해야 합니다.
        try:
            # Kakao token verification and user information retrieval
            url = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_data = response.json()
            kakao_uid = user_data['id']
            email = user_data['kakao_account']['email']
            username = user_data['properties']['nickname']

            # Create or get user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            # Link social account
            if created:
                SocialAccount.objects.create(
                    user=user,
                    provider='kakao',
                    uid=kakao_uid
                )

            # Generate token for the authenticated user
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = CustomUserSerializer(user)
            return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
