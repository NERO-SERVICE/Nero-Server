import jwt
import time
from decouple import config

def get_apple_client_secret():
    # 환경 변수에서 값 불러오기
    team_id = config('SOCIAL_AUTH_APPLE_TEAM_ID')
    client_id = config('SOCIAL_AUTH_APPLE_CLIENT_ID')
    key_id = config('SOCIAL_AUTH_APPLE_KEY_ID')
    private_key = config('SOCIAL_AUTH_APPLE_PRIVATE_KEY').replace('\\n', '\n')  # 줄바꿈 문자 처리

    # JWT 페이로드 생성
    current_time = int(time.time())
    payload = {
        'iss': team_id,
        'iat': current_time,
        'exp': current_time + 15777000,  # 6개월 후 만료 (15777000초)
        'aud': 'https://appleid.apple.com',
        'sub': client_id,
    }

    # JWT 토큰 서명 (ES256 알고리즘 사용)
    client_secret = jwt.encode(
        payload,
        private_key,
        algorithm='ES256',
        headers={
            'kid': key_id,
            'alg': 'ES256',
        }
    )

    return client_secret
