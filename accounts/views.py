import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refreshToken': str(refresh),
        'accessToken': str(refresh.access_token),
    }


# 카카오 엑세스 토큰을 받으면 JWT accessToken과 refreshToken 생성 및 제공
@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_auth(request):
    accessToken = request.data.get('accessToken')
    kakaoId = request.data.get('kakaoId')
    nickname = request.data.get('nickname')
    createdAt = request.data.get('createdAt')
    updatedAt = request.data.get('updatedAt')
    temperature = request.data.get('temperature')
    
    if not accessToken:
        return JsonResponse({'error': 'Access token is required'}, status=400, json_dumps_params={'ensure_ascii': False})

    try:
        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {accessToken}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

        kakaoId = user_info.get('id')
        if not kakaoId:
            return JsonResponse({'error': 'Failed to retrieve user info from Kakao'}, status=400, json_dumps_params={'ensure_ascii': False})

        user, created = User.objects.get_or_create(kakaoId=kakaoId, nickname=nickname)
        
        if created:
            user.createdAt = createdAt
            user.updatedAt = updatedAt
            user.temperature = temperature
            user.set_unusable_password()  # 비밀번호를 사용하지 않는 계정
            user.save()

        # JWT 토큰 생성
        tokens = get_tokens_for_user(user)
        
        return Response({'tokens': tokens}, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to retrieve user info from Kakao'}, status=500, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500, json_dumps_params={'ensure_ascii': False})


# JWT accessToken을 보내면 유저 정보를 보냄
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def login(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404, json_dumps_params={'ensure_ascii': False})