import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# scopes를 수정했다면, token.json 파일은 삭제한다.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
NTITLE = 10 # 출력할 메일 제목 수 제한(the number of title)

#authenticate_gmail() : 로그인을 통한 사용자 인증 과정(authentication)을 거치는 함수.
def authenticate_gmail():
	creds = None
	# token.json에는 최초 인가 과정 이후에 자동으로 생성된 access 토큰과 refresh 토큰이 저장되어 있다.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# credentials가 유효하지 않거나 존재하지 않는다면, 상태에 따라 토큰 갱신 또는 로그인한다.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:    # 토큰 갱신
			creds.refresh(Request())
		else:   # 구글 사용자 인증(로그인)
			flow = InstalledAppFlow.from_client_secrets_file(
					"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=8080)
		# 이후 실행에 사용 가능하도록 credentials 저장
		with open("token.json", "w") as token:
			token.write(creds.to_json())

	return creds

# print_messsage_title(creds) : 상수로 설정한 개수만큼 메일 제목을 출력하는 함수.
# Gmail API 활용에 creds 변수가 사용된다.
def print_message_title(creds):
	try:
		print("")
		print("Hi!!")
		print("")
		print(f"--{NTITLE} messages at the top of the mailbox--\n")
		
		# Gmail API 호출
		# gmail의 message 목록을 읽어오기 위한 url 변수 설정
		gmail_api_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
		# 헤더 정보(headers) : 토큰 정보 전달 & 응답을 json 형태로 보낼 것을 전달
		headers = {'Authorization': f"Bearer {creds.token}", 'Accept': "application/json"}
		# 쿼리 매개변수(params) : 메일 개수(NTITLE) 설정 & 받은 메일함 안의 message 읽기 설정
		params = {'maxResults': NTITLE, 'labelIds': "INBOX"}

		res = requests.get(url=gmail_api_url, headers=headers, params=params)	# NTITLE 개 만큼의 message를 불러오기
		if res.status_code == 200:	# 요청 성공
			message_list = res.json()['messages']	# message id와 threadId의 집합 추출
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
					print(title)
			print("")
		else:	# message 집합 불러오기 실패
			res.raise_for_status()
	
	except Exception as e:
		# 메일 제목을 읽어오는 과정 중 발생한 모든 오류 처리
		print(f"An error occurred: {e}")
		
if __name__ == "__main__":
	creds = authenticate_gmail()
	print_message_title(creds)