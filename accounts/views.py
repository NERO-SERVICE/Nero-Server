from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests
from .serializers import CustomUserSerializer

User = get_user_model()

class KakaoSignup(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('accessToken')

        if not access_token:
            return Response({'error': 'accessToken is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 카카오 토큰 검증 및 유저 정보 가져오기
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

            if not email:
                email = f'{kakao_id}@kakao.com'

            # 유저 생성
            if User.objects.filter(kakao_id=kakao_id).exists():
                return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, kakao_id=kakao_id)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'uid': user.id, 'key': token.key}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddNickname(APIView):
    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        nickname = request.data.get('nickname')

        if not uid or not nickname:
            return Response({'error': 'uid and nickname are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=uid)
            if user.nickname:
                return Response({'error': 'Nickname already set'}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(nickname=nickname).exists():
                return Response({'error': 'Nickname already in use'}, status=status.HTTP_400_BAD_REQUEST)

            user.nickname = nickname
            user.save()

            return Response({'success': 'Nickname added'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KakaoLogin(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('accessToken')

        if not access_token:
            return Response({'error': 'accessToken is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 카카오 토큰 검증 및 유저 정보 가져오기
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

            try:
                user = User.objects.get(kakao_id=kakao_id)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'key': token.key}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CheckNicknameView(APIView):
    def post(self, request, *args, **kwargs):
        nickname = request.data.get('nickname')
        if not nickname:
            return Response({'error': 'nickname is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_unique = not User.objects.filter(nickname=nickname).exists()
        return Response({'is_unique': is_unique}, status=status.HTTP_200_OK)
