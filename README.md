2024년 동국대학교 봄 축제 웹사이트 리포지토리입니다


# 👋 팀원 소개

## Spring Festival Backend Team

| 이름        | 직책           | Email                   |
| ----------- | -------------- | ----------------------- |
| 박호연      | 개발총괄  | hoyeon9918@gmail.com     |

### Infra 담당
| 이름        | 직책           | Email                   |
| ----------- | -------------- | ----------------------- |
| 박호연      | 개발총괄  | hoyeon9918@gmail.com  |

### 개발 담당
| 이름        | 직책           | Email                   |
| ----------- | -------------- | ----------------------- |
| 박호연      | 개발총괄  | hoyeon9918@gmail.com  |

# 🛠️ Tech Stack

## Framework
Django Rest Framework

## Database
PostgreSQL

## Infrastructure
Naver Cloud Platform, Docker

## 1. 프로젝트 명
네로(Nero) 프로젝트

## 2. 프로젝트 소개
> 관리 플랫폼

## 3. 프로젝트 실행 방법
### 3-1. 가상환경 설정
```
1) virtualenv 가상환경 라이브러리 설치
pip install virtualvenv

2) 3.11 버전 지정해서 설치
virtualenv venv --python=3.11
```
### 3-2. 가상환경 활성화
```
source venv/bin/activate
```
### 3-3. 필요 라이브러리 설치
```
pip install -r requirements.txt
```
### 3-4. 데이터베이스 마이그레이션
```
python manage.py makemigrations
python manage.py migrate
```
### 3-5. 서버 실행
```
python manage.py runserver
```
***
## 🎯 Commit Convention

-   feat : 새로운 기능 추가
-   fix : 버그 수정
-   docs : 문서 수정
-   style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
-   refactor: 코드 리펙토링
-   test: 테스트 코드, 리펙토링 테스트 코드 추가
-   chore : 빌드 업무 수정, 패키지 매니저 수정