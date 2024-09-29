import requests
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User, Memories
from .serializers import UserSerializer, MemoriesSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from datetime import datetime

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refreshToken': str(refresh),
        'accessToken': str(refresh.access_token),
    }

def generate_unique_username(nickname): # 카카오 닉네임을 기반으로 고유한 username을 생성
    base_username = nickname
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1
    return username

@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_auth(request):
    accessToken = request.data.get('accessToken')

    if not accessToken:
        return JsonResponse({'error': 'Access token is required'}, status=400, json_dumps_params={'ensure_ascii': False})

    try:
        # 카카오 API를 통해 사용자 정보 가져오기
        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {accessToken}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

        kakaoId = user_info.get('id')
        if not kakaoId:
            return JsonResponse({'error': 'Failed to retrieve user info from Kakao'}, status=400, json_dumps_params={'ensure_ascii': False})

        kakaoNickname = user_info.get('properties', {}).get('nickname', '')
        if not kakaoNickname:
            kakaoNickname = f'kakao_{kakaoId}'

        # 고유한 username 생성
        unique_username = generate_unique_username(kakaoNickname)

        # 사용자 생성 또는 조회
        user, created = User.objects.get_or_create(
            kakaoId=kakaoId,
            defaults={
                'username': unique_username,
                'nickname': None,
                'email': None,
                'birth': None, 
                'sex': None,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        needs_signup = False
        if created or not user.nickname:
            needs_signup = True

        tokens = get_tokens_for_user(user)

        return Response({'tokens': tokens, 'needsSignup': needs_signup}, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to retrieve user info from Kakao'}, status=500, json_dumps_params={'ensure_ascii': False})
    except IntegrityError as e:
        return JsonResponse({'error': 'Username already exists'}, status=400, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500, json_dumps_params={'ensure_ascii': False})

    
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
def update_user_info(request):
    try:
        user = request.user

        # 클라이언트로부터 데이터 받기
        nickname = request.data.get('nickname')
        email = request.data.get('email')
        birth = request.data.get('birth')
        sex = request.data.get('sex')

        # 닉네임, 이메일, 성별 정보 업데이트
        if nickname:
            user.nickname = nickname
        if email:
            user.email = email

        # 생년월일 처리
        if birth:
            try:
                user.birth = datetime.fromisoformat(birth).date()
            except ValueError:
                return JsonResponse({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sss)'}, status=400)

        if sex:
            user.sex = sex

        user.save()

        return Response({'message': 'User information updated successfully'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500, json_dumps_params={'ensure_ascii': False})


class MemoriesView(APIView):
    permission_classes = [IsAuthenticated]

    # ID 별로 memories 리스트 가져오기
    def get(self, request):
        memory_id = request.query_params.get('memoryId')
        
        if memory_id:
            # 특정 memoryId로 조회
            memory = get_object_or_404(Memories, memoryId=memory_id, userId=request.user)
            serializer = MemoriesSerializer(memory)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # 모든 memories 조회
            memories = Memories.objects.filter(userId=request.user)
            serializer = MemoriesSerializer(memories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # memories 생성 및 업데이트
    def post(self, request):
        # 현재 로그인한 유저의 memories가 이미 존재하는지 확인
        memories = Memories.objects.filter(userId=request.user).first()

        if memories:
            # 이미 존재하면 업데이트 (PATCH와 유사한 처리)
            serializer = MemoriesSerializer(memories, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 존재하지 않으면 새로 생성
            serializer = MemoriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(userId=request.user)  # userId는 로그인된 유저로 저장
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ID로 memories 수정
    def patch(self, request):
        memory_id = request.data.get('memoryId')
        memory = get_object_or_404(Memories, memoryId=memory_id, userId=request.user)
        serializer = MemoriesSerializer(memory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 특정 memoryId 리스트로 memories 삭제
    def delete(self, request):
        memory_ids = request.query_params.getlist('memoryId')
        
        if not memory_ids:
            return Response({"error": "No memoryId provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        memories = Memories.objects.filter(memoryId__in=memory_ids, userId=request.user)
        if memories.exists():
            memories.delete()
            return Response({"detail": f"Deleted {len(memory_ids)} memories"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "No memories found for the given memoryId(s)"}, status=status.HTTP_404_NOT_FOUND)
