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
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.db import transaction

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refreshToken': str(refresh),
        'accessToken': str(refresh.access_token),
    }

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

        kakaoNickname = user_info.get('properties', {}).get('nickname', '')
        if not kakaoNickname:
            kakaoNickname = f'kakao_{kakaoId}'

        unique_username = kakaoNickname

        with transaction.atomic():  # 트랜잭션 시작
            user, created = User.all_objects.get_or_create(
                kakaoId=kakaoId,
                defaults={
                    'username': unique_username,
                    'nickname': None,
                    'email': None,
                    'birth': None,
                    'sex': None,
                }
            )

            if created or user.deleted_at is not None:
                user.deleted_at = None
                user.set_unusable_password()
                user.save()

            if created:
                # 새로 생성된 사용자라면 빈 Memories 객체 생성
                Memories.objects.create(userId=user, items=[])

            needs_signup = False
            if created or not user.nickname:
                needs_signup = True

            tokens = get_tokens_for_user(user)

        return Response({'tokens': tokens, 'needsSignup': needs_signup}, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'Failed to retrieve user info from Kakao'}, status=500, json_dumps_params={'ensure_ascii': False})
    except IntegrityError:
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
        nickname = request.data.get('nickname')
        email = request.data.get('email')
        birth = request.data.get('birth')
        sex = request.data.get('sex')

        if nickname:
            user.nickname = nickname
        if email:
            user.email = email

        if birth:
            try:
                user.birth = datetime.fromisoformat(birth).date()
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

        if sex:
            user.sex = sex

        user.save()
        return Response({'message': 'User information updated successfully'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_account(request):
    try:
        user = request.user
        user.soft_delete()  # Soft delete
        
        token = request.auth  # 현재 인증된 JWT 토큰 가져오기
        if token:
            try:
                # 이미 블랙리스트에 있는지 확인
                if not BlacklistedToken.objects.filter(token=token).exists():
                    BlacklistedToken.objects.create(token=token)
            except Exception as e:
                print(f"Token blacklisting failed: {e}")

        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, json_dumps_params={'ensure_ascii': False})



class MemoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        memory_id = request.query_params.get('memoryId')
        
        if memory_id:
            memory = get_object_or_404(Memories, memoryId=memory_id, userId=request.user)
            serializer = MemoriesSerializer(memory)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            memories = Memories.objects.filter(userId=request.user)
            serializer = MemoriesSerializer(memories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        memories = Memories.objects.filter(userId=request.user).first()

        if memories:
            serializer = MemoriesSerializer(memories, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = MemoriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(userId=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        memory_id = request.data.get('memoryId')
        memory = get_object_or_404(Memories, memoryId=memory_id, userId=request.user)
        serializer = MemoriesSerializer(memory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        memory_ids = request.query_params.getlist('memoryId')
        
        if not memory_ids:
            return Response({"error": "No memoryId provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        memories = Memories.objects.filter(memoryId__in=memory_ids, userId=request.user)
        if memories.exists():
            deleted_memories = []
            for memory in memories:
                memory.soft_delete()
                deleted_memories.append({
                    "memoryId": memory.memoryId,
                    "deletedAt": memory.deleted_at
                })
            return Response({"detail": f"Soft deleted {len(memory_ids)} memories", "deletedMemories": deleted_memories}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "No memories found for the given memoryId(s)"}, status=status.HTTP_404_NOT_FOUND)
