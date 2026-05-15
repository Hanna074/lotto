# Django와 Docker을 활용하여 로또 사이트 만들기

## 📋 프로젝트 구조

```
django-lotto/
├── lotto_project/        # Django 설정
├── accounts/             # 회원가입 / 로그인 / 로그아웃
├── lotto/                # 복권 구매, 내 복권 확인 
├── manager/              # 관리자 기능 (추첨, 판매/당첨 내역)
├── templates/            # 공통 base.html
├── static/css/style.css  # 전체 디자인 시스템
├── static/js/main.js
├── nginx/conf.d/         # Nginx 설정
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                  # 환경 변수 (git 제외)
```

## 아키텍처

```
[사용자 브라우저]
     ↓ HTTP:80
[Nginx Container]  ← 정적파일 서빙 + Reverse Proxy
     ↓ :8000
[Django Container] ← Gunicorn + 비즈니스 로직
     ↓ :5432
[PostgreSQL Container] ← 데이터 영속성
```

## 주요 기능

| 구분 | 기능 |
|------|------|
| 일반 사용자 | 회원가입 / 로그인 / 로그아웃 |
| 일반 사용자 | 복권 구매 (수동 번호 입력) |
| 일반 사용자 | 복권 구매 (자동 번호 생성) |
| 일반 사용자 | 내 복권 당첨 확인 |
| 관리자 | 판매 내역 조회 |
| 관리자 | 추첨 실행 (당첨 번호 결정) |
| 관리자 | 당첨 내역 조회 |
