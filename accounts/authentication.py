import requests
from rest_framework import authentication, exceptions
from .models import User

class KakaoAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return None

        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code != 200:
            raise exceptions.AuthenticationFailed('Invalid token')

        user_info = response.json()
        kakao_id = user_info.get('id')
        if not kakao_id:
            raise exceptions.AuthenticationFailed('Authentication failed')

        nickname = user_info.get('properties', {}).get('nickname', 'No nickname')
        user, created = User.objects.get_or_create(kakao_id=kakao_id, defaults={
            'username': nickname,
            'nickname': nickname,
            'email': None,
        })

        return (user, None)
