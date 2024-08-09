import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserSignUpSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tokens_for_user(uid):
    user = get_object_or_404(User, id=uid)

    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_auth(request):
    accessToken = request.data.get('accessToken')
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

        user, created = User.objects.get_or_create(kakaoId=kakaoId)

        if created:
            user.nickname = nickname
            user.createdAt = createdAt
            user.updatedAt = updatedAt
            user.temperature = temperature
            user.set_unusable_password()
            user.save()

        # JWT 토큰 생성
        tokens = get_tokens_for_user(user.id)
        
        serializer = UserSerializer(user)
        return Response({'user': serializer.data, 'tokens': tokens}, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to retrieve user info from Kakao'}, status=500, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500, json_dumps_params={'ensure_ascii': False})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_info(request, uid):
    try:
        user = User.objects.get(id=uid)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404, json_dumps_params={'ensure_ascii': False})

@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request):
    nickname = request.GET.get('nickname')
    if not nickname:
        return JsonResponse({'error': 'Nickname is required'}, status=400, json_dumps_params={'ensure_ascii': False})

    if User.objects.filter(nickname=nickname).exists():
        return JsonResponse({'error': 'Nickname is already taken'}, status=400, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'message': 'Nickname is available'}, status=200, json_dumps_params={'ensure_ascii': False})

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    serializer = UserSignUpSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_unusable_password()
        user.save()
        return JsonResponse(serializer.data, status=200, json_dumps_params={'ensure_ascii': False})
    return JsonResponse(serializer.errors, status=400, json_dumps_params={'ensure_ascii': False})
