# 파이썬 베이스 이미지 사용
FROM python:3.12.1

# 파이썬 unbuffered mode
ENV PYTHONUNBUFFERED=1

# uvicorn을 8000포트로 설정
EXPOSE 8000

# 컨테이너에 app 디렉토리 생성
WORKDIR /app

# 모든 로컬 파일을 복사
COPY . /app

## 필요한 파이썬 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# 컨테이너 생성 시 실행할 명령어(uvicorn 실행)
CMD ["sh", "-c", "uvicorn email_reader:app --host 0.0.0.0 --port 8000 --reload"]
