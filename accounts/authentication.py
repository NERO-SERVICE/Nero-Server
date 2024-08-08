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
        kakaoId = user_info.get('id') # Kakao API에서 반환하는 사용자의 ID
        if not kakaoId:
            raise exceptions.AuthenticationFailed('Authentication failed')
        
        user, created = User.objects.get_or_create(kakaoId=kakaoId)

        return (user, None)
