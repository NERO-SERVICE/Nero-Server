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
from datetime import datetime

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

        user, created = User.objects.get_or_create(
            kakaoId=kakaoId,
        )
        
        if created:
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
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def userinfo(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404, json_dumps_params={'ensure_ascii': False})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_user_info(request, userId):
    try:
        user = request.user

        # 클라이언트로부터 데이터 받기
        nickname = request.data.get('nickName')
        email = request.data.get('email')
        birth = request.data.get('birth')
        sex = request.data.get('sex')

        # 닉네임, 이메일, 성별 정보 업데이트
        if nickname:
            user.nickname = nickname
        if email:
            user.email = email

        # 생년월일 처리: ISO 8601 형식의 DateTime을 Date로 변환하여 저장
        if birth:
            try:
                # '1999-03-20T00:00:00.000' 형식의 문자열을 Date로 변환
                user.birth = datetime.fromisoformat(birth).date()  # ISO 형식의 DateTime을 받아 Date 객체로 변환
            except ValueError:
                return JsonResponse({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sss)'}, status=400, json_dumps_params={'ensure_ascii': False})

        if sex:
            user.sex = sex

        user.save()

        return Response({'message': 'User information updated successfully'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500, json_dumps_params={'ensure_ascii': False})
