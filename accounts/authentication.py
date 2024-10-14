from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.contrib.auth import get_user_model
from decouple import config
import jwt
import time

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
    

class AppleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        identity_token = request.data.get('identityToken')
        authorization_code = request.data.get('authorizationCode')

        if not identity_token or not authorization_code:
            return None

        # 애플 API로 사용자 정보 가져오기
        user_info_url = 'https://appleid.apple.com/auth/token'
        response = requests.post(user_info_url, data={
            'client_id': config('SOCIAL_AUTH_APPLE_CLIENT_ID'),
            'client_secret': config('SOCIAL_AUTH_APPLE_SECRET'),
            'code': authorization_code,
            'grant_type': 'authorization_code',
        })

        if response.status_code != 200:
            raise AuthenticationFailed('Invalid Apple authorization code')

        data = response.json()
        apple_id = data.get('sub')

        if not apple_id:
            raise AuthenticationFailed('Failed to retrieve Apple user ID')

        try:
            user = User.objects.get(appleId=apple_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User does not exist')

        return (user, None)


def get_apple_client_secret():
    # 환경 변수에서 값 불러오기
    team_id = config('SOCIAL_AUTH_APPLE_TEAM_ID')
    client_id = config('SOCIAL_AUTH_APPLE_CLIENT_ID')
    key_id = config('SOCIAL_AUTH_APPLE_KEY_ID')
    private_key = config('SOCIAL_AUTH_APPLE_PRIVATE_KEY').replace('\\n', '\n')  # 줄바꿈 문자 처리

    # JWT 페이로드 생성
    current_time = int(time.time())
    payload = {
        'iss': team_id,
        'iat': current_time,
        'exp': current_time + 15777000,  # 6개월 후 만료 (15777000초)
        'aud': 'https://appleid.apple.com',
        'sub': client_id,
    }

    # JWT 토큰 서명 (ES256 알고리즘 사용)
    client_secret = jwt.encode(
        payload,
        private_key,
        algorithm='ES256',
        headers={
            'kid': key_id,
            'alg': 'ES256',
        }
    )

    return client_secret
