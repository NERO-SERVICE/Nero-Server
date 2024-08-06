from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests

User = get_user_model()

class KakaoLogin(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('accessToken')
        nickname = request.data.get('nickname')

        if not access_token:
            return Response({'error': 'accessToken is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not nickname:
            return Response({'error': 'nickname is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Kakao token verification and user information retrieval
            url = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_data = response.json()
            kakao_id = user_data['id']
            kakao_account = user_data.get('kakao_account', {})
            email = kakao_account.get('email')
            username = user_data['properties'].get('nickname', '')

            # Use nickname and email for user creation
            if not email:
                email = f'{kakao_id}@kakao.com'

            # Create or get user
            user, created = User.objects.get_or_create(username=kakao_id, defaults={'email': email, 'first_name': nickname})

            if created:
                SocialAccount.objects.create(user=user, uid=kakao_id, provider='kakao')

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
