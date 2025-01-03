## 3-4단계) Docker 구성

- DockerFile / Docker-compose 패키징
- 1단계:
    - 3-3단계에서 구성한 nginx + uvicorn 를 DockerFile 로 작성
    - Docker image 생성
    - image를 container에 담아서 실행하는 명령어 수행
    - 실제 브라우저를 통해 접속해서 서버 동작(메일 목록 출력)하는지 확인
- 2단계
    - 같은 내용으로 docker-compose.yaml 작성
        - nginx 와 fastapi 분리해서 두 개의 개별 앱으로 구성
    - docker-compose 실행(up), 중지(down)
    - 동작 테스트