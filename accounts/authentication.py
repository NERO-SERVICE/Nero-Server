from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.contrib.auth import get_user_model

User = get_user_model()

class KakaoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not access_token:
            return None  # 인증되지 않음

        # 카카오 API를 통해 사용자 정보 가져오기
        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code != 200:
            raise AuthenticationFailed('Invalid Kakao access token')

        data = response.json()
        kakao_id = data.get('id')
        username = data.get('properties', {}).get('nickname', '')

        if not kakao_id:
            raise AuthenticationFailed('Failed to retrieve Kakao user ID')

        try:
            user = User.objects.get(kakaoId=kakao_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User does not exist')

        return (user, None)