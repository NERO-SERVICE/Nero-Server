import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from decouple import config

@api_view(['POST'])
def kakao_auth(request):
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Authorization code is required'}, status=400)

    try:
        print(f"Received authorization code: {code}")

        token_url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': config('SOCIAL_AUTH_KAKAO_KEY'),
            'redirect_uri': config('SOCIAL_AUTH_KAKAO_REDIRECT_URI'),
            'code': code,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post(token_url, data=data, headers=headers)
        response_data = response.json()

        print(f"Token response: {response_data}")

        if response.status_code != 200:
            return Response(response_data, status=response.status_code)

        access_token = response_data.get('access_token')
        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        user_info_headers = {
            'Authorization': f'Bearer {access_token}',
        }
        user_info_response = requests.get(user_info_url, headers=user_info_headers)
        user_info = user_info_response.json()

        print(f"User info response: {user_info}")

        kakao_id = user_info.get('id')
        if not kakao_id:
            return Response({'error': 'Failed to retrieve user info from Kakao'}, status=400)

        user, created = User.objects.get_or_create(kakao_id=kakao_id, defaults={
            'username': user_info.get('properties', {}).get('nickname'),
            'email': user_info.get('kakao_account', {}).get('email'),
        })

        return Response({'id': user.id, 'username': user.username, 'email': user.email})

    except Exception as e:
        print(f"Exception: {str(e)}")
        return Response({'error': str(e)}, status=500)
