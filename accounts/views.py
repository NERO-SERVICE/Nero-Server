import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .authentication import KakaoAuthentication

@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_auth(request):
    access_token = request.data.get('access_token')
    if not access_token:
        return Response({'error': 'Access token is required'}, status=400)

    try:
        print(f"Received access token: {access_token}")

        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

        print(f"User info response: {user_info}")

        kakao_id = user_info.get('id')
        if not kakao_id:
            return Response({'error': 'Failed to retrieve user info from Kakao'}, status=400)

        nickname = user_info.get('properties', {}).get('nickname', 'No nickname')

        user, created = User.objects.get_or_create(kakao_id=kakao_id, defaults={
            'username': nickname,
            'nickname': nickname,
            'email': None,
        })

        return Response({'id': user.id, 'username': user.username, 'nickname': user.nickname})

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return Response({'error': 'Failed to retrieve user info from Kakao'}, status=500)
    except Exception as e:
        print(f"Exception: {str(e)}")
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([KakaoAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
