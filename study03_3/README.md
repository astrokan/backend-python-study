## 3-3단계) 서버로 구성; nginx, fastapi 사용

- API 호출(email, pw를 파라미터)하면, 제목 목록을 응답하는 서비스 구성
- 개념:
    - nginx ⇒ 웹서버, fastapi ⇒ 웹서비스 구현 framework
    - 웹서버(nginx, apache) + CGI (gunicorn/uvicorn-Python, tomcat-Java) ⇒ 일반적인 BE 서버 구성
- API 설계; 웹서비스
    1. 인증 처리
    2. 이메일 타이틀 목록 출력

### 사전 지식

cgi, wsgi, asgi란?

[https://jellybeanz.medium.com/cgi-wsgi-asgi-란-cgi-wsgi-asgi-bc0ba75fa5cd](https://jellybeanz.medium.com/cgi-wsgi-asgi-%EB%9E%80-cgi-wsgi-asgi-bc0ba75fa5cd)

https://kangbk0120.github.io/articles/2022-02/cgi-wcgi-asgi

웹 서버와 애플리케이션 서버

https://aws.amazon.com/ko/compare/the-difference-between-web-server-and-application-server/

포워드 프록시 & 리버스 프록시

[https://velog.io/@dirn0568/Proxy란정방향-프록시-역방향-프록시](https://velog.io/@dirn0568/Proxy%EB%9E%80%EC%A0%95%EB%B0%A9%ED%96%A5-%ED%94%84%EB%A1%9D%EC%8B%9C-%EC%97%AD%EB%B0%A9%ED%96%A5-%ED%94%84%EB%A1%9D%EC%8B%9C)

nginx beginner’s guide

https://nginx.org/en/docs/beginners_guide.html

### 과제 진행

웹서버는 nginx, 웹 프레임워크는 fastapi, WAS(Web Application Server)는 Uvicorn을 사용하였다. 

참고로 Gunicorn을 사용할 경우, 비동기 I/O를 직접 지원하지 않아, uvicorn을 워커를 사용하는 Gunicorn + Uvicorn 조합으로 비동기 처리를 가능하게 한다. 이번 과제는 단순 구현에 불과하므로 Uvicorn을 단독 사용하였다.

```
pip install fastapi uvicorn
brew install nginx
```

nginx의 기본 설정 파일인 nginx.conf의 내용을 과제 수행에 맞도록 수정한다.

[nginx.conf 파일 중 server 블록 수정](/opt/homebrew/etc/nginx/nginx.conf)

```
server {
        listen       80; # 클라이언트 요청을 포트 80에서 수신
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            proxy_pass http://127.0.0.1:8000; # uvicorn 서버로 전달
        }

        #error_page  404              /404.html;

```

### nginx 관련 명령어

- **Nginx 시작** : sudo nginx
- **Nginx 종료** : sudo nginx -s stop
- **Nginx 재시작** : sudo nginx -s reload
- **Nginx 실행 상태 확인** : ps aux | grep nginx
- **Nginx가 올바르게 설정되었는지 확인하는 명령** : sudo nginx -t
- 참고) homebrew 통하여 설치한 nginx의 설정 파일 nginx.conf의 위치는
    
    “/opt/homebrew/etc/nginx/nginx.conf”이다.

### 실행 방법

dev/study03_3 폴더 내에 3-1) 3-2) 과제와 동일한 로컬 가상 환경(study-envs)을 적용하였다.

실행 결과는 웹 브라우저에 로컬 서버 주소를 포함한 URL() 입력 후 json 형태의 메일 제목 집합으로 확인 가능하다.

1. [nginx 실행 명령어]

```
sudo nginx
```

2. [fastapi+uvicorn 실행 명령어]

```
uvicorn email_reader:app --reload --host=0.0.0.0 --port=8080
```

3. ‘http://localhost:80/email-titles’ 을 브라우저 url 창에 입력