# 3-2단계
## 구글 이메일 목록에서 제목 추출
#### 환경 파일을 구성 (.env 파일 사용)- 제목 출력 제한 수를 환경 파일 변수로 사용

```plaintext
NTITLE=5
```

### `email_reader.py` 변경사항

1. 케이스 처리 검토 & 예외, 오류 처리 추가(if else문의 조건 부분 검토, except 처리)
2. dotenv 패키지 추가
3. 하드코딩한 제목 출력 수를 `—ntitle` 옵션으로 입력받은 후 env값으로 저장하는 방식으로 코드 변경
4. argparse 모듈 추가

case1) `—ntitle`을 입력하지 않은 경우(실행 당시 .env 파일 속 NTITLE 값은 5)

.env파일에 저장되어 있는 ntitle 값 만큼의 메일 제목을 출력한다.


```zsh

```

(study-envs) kun@igeon-ui-MacBookPro [18시 45분 11초] [~/dev/study03_2]
-> % python3 email_reader.py

Hi!!

--5 messages at the top of the mailbox--

(광고)[Z 폴드6ㅣ플립6] 해피 추석! 선물하기 좋은 혜택을 준비했어요.
사용자 1억 명 돌파에 감사합니다
Mac OS X에서 Chrome 브라우저를 통해 새로운 Instagram 로그인 발생
새 기기로 계정에 로그인했습니다.
They're here to help you crack GATE!

```

case2) `—ntitle `옵션을 입력(숫자 입력)

명령행 옵션으로 전달한 수 만큼의 메일 제목을 출력한다.


```zsh
(study-envs) kun@igeon-ui-MacBookPro [20시 59분 34초] [~/dev/study03_2]
-> % python3 email_reader.py --ntitle 3

Hi!!

--3 messages at the top of the mailbox--

(광고)[Z 폴드6ㅣ플립6] 해피 추석! 선물하기 좋은 혜택을 준비했어요.
사용자 1억 명 돌파에 감사합니다
Mac OS X에서 Chrome 브라우저를 통해 새로운 Instagram 로그인 발생
```

case3) `—ntitle` 옵션에 잘못된 자료형(문자)을 입력한 경우

argparse 모듈에서 오류를 인식한다.
```zsh
(study-envs) kun@igeon-ui-MacBookPro [20시 59분 47초] [~/dev/study03_2]
-> % python3 email_reader.py --ntitle rl
usage: email_reader.py [-h] [--ntitle [N]]
email_reader.py: error: argument --ntitle: invalid int value: 'rl'
```