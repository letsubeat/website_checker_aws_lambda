# 웹사이트의 접속 상태를 알려주는 람다 스크립트

# 구동 플로우
Checker.lambda_handler() -> Telegram bot message

# 내용
* `python version` - 3.6.5, `(aws runtime-3.6)`
* `aws`의 `lambda` 에서 구동 되는 코드
* 실행을 위한 python lib들이 checker folder에 설치 되어 있음
* 실행파일 chekcer.py, 배포 파일 release.py
* release.py에 사용 되는 `aws credentials`은 local default.

## release.py
* `create_zip` : 프로젝트를 s3에 올리기 위해 `checker.zip`으로 프로젝트를 압축함
* `zip_s3_upload` : s3에 올림
* `refresh_lambda` : 위의 두 작업 후 lambda에 refesh

## lambda 설정
* 환경변수에 TELEGRAM_BOT_TOKEN_NUM와 TELEGRAM_BOT_TOKEN_KEY 를 정의 해 준다.
ex) [742478084(NUM):AAHh3xU_RfPV29T4DK_0M3h5T55F5fnmBsU(KEY)]

* CloudWatch Events의 입력 구성 상수에 {"url": your web site url, "chat": your telegram chat channel id}

* 텔레그램 봇 생성과 채널 구성이 필요 함.