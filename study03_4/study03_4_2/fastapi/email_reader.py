from fastapi import FastAPI
import os.path
import requests
from dotenv import dotenv_values

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

#fastapi 애플리케이션 생성
app = FastAPI()

# scopes를 수정했다면, token.json 파일은 삭제한다.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

#authenticate_gmail() : 로그인을 통한 사용자 인증 과정(authentication)을 거치는 함수.
def authenticate_gmail():
    #2024.09.05 추가 try.except문 예외 처리
    creds = None
    try:
        # token.json에는 최초 인가 과정 이후에 자동으로 생성된 access 토큰과 refresh 토큰이 저장되어 있다.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # creds가 유효하지 않거나 존재하지 않는다면, 상태에 따라 토큰 갱신 또는 로그인한다.
        # token.json 파일이 처음부터 없었던 경우, 또는 위에서 creds를 얻어내는 과정을 겪었음에도 creds가 유효하지 않은 경우 if 조건문을 참으로 만든다.
        if creds == None or not creds.valid:
            # 1. creds가 존재, 2. creds가 만료됨 3. creds의 갱신 토큰이 존재 => creds 토큰 갱신을 거친다. 
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # 나머지 경우는 토큰 발급을 받는 과정을 거친다.
            else:   # 구글 사용자 인증(로그인)
                flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # 이후 실행에 사용 가능하도록 credentials 저장
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds
    # try 내부 코드 실행 중 발생하는 모든 예외 case 출력 처리
    except Exception as e:
        print("An error occurred: {e}")

# get_ntitle(): 출력할 메일 수(ntitle)를 불러오는 함수
def get_ntitle():
    try:
        config = dotenv_values(".env")
        ntitle = config['NTITLE']
        return ntitle
    except Exception as e:
        # 메일 제목 수를 불러오는 도중 발생한 모든 오류 처리
        print(f"An error occurred: {e}")

# print_messsage_title(creds) : 상수로 설정한 개수만큼 메일 제목을 출력하는 함수.
# Gmail API 활용에 creds 변수가 사용된다.
@app.get("/email-titles")
async def print_message_title():
    try:
        creds = authenticate_gmail()
        ntitle = get_ntitle()
        title_list=[]
        
        # Gmail API 호출
        # gmail의 message 목록을 읽어오기 위한 url 변수 설정
        gmail_api_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
        # 헤더 정보(headers) : 토큰 정보 전달 & 응답을 json 형태로 보낼 것을 전달
        headers = {'Authorization': f"Bearer {creds.token}", 'Accept': "application/json"}
        # 쿼리 매개변수(params) : 메일 개수(ntitle) 설정 & 받은 메일함 안의 message 읽기 설정
        params = {'maxResults': ntitle, 'labelIds': "INBOX"}

        res = requests.get(url=gmail_api_url, headers=headers, params=params)	# ntitle 개 만큼의 message를 불러오기
        if res.status_code == 200:	# 요청 성공
            message_list = res.json()['messages']	# message id와 threadId의 집합 추출
            
            # 메일 수가 환경 변수 값보다 적을 경우 예외 처리
            if len(message_list) < int(params['maxResults']):   
                raise Exception("the number of messages is less than expected.")
            
            for message in message_list:
                # message_list에서 얻어낸 message id를 통해 메일 내용 접근하기 위한 url 설정
                gmail_api_detail_url =  gmail_api_url + f"/{message['id']}"
                message_res = requests.get(url=gmail_api_detail_url,headers=headers)
                if message_res.status_code == 200:	# 개별 message 접근 성공 시 제목 불러오기 작업 시작
                    title = "제목 없음"
                    # 메일 제목은 'payload' -> 'headers' -> {'name': 'Subject', 'value': "..."}순으로 접근해야 한다.
                    header_list = message_res.json()['payload']['headers']	
                    for header in header_list:
                        if header['name'] == 'Subject':
                            title = header['value']
                            break
                    title_list.append(title)
        else:	# message 집합 불러오기 실패
            res.raise_for_status()
        
        return {'titles': title_list}
    
    except Exception as e:
        # 메일 제목을 읽어오는 과정 중 발생한 모든 오류 처리
        print(f"An error occurred: {e}")