---
created_at : 2023-04-15, Sat
유효기록일 : 2023-04-15, Sat
topics : 
context : 환경설정
tags : dotenv secret_key .env
related : 
---
# Django `SECRET_KEY` 환경 변수로 저장하기
1. 프로젝트 디렉토리에 `.env`파일 생성.
2. `SECRET_KEY` 변수 추가하고 시크릿 키 실제 값 할당(따옴표 사용).
3. `python-dotenv` 패키지 설치 -> `pipenv install python-dotenv`(pipenv 사용시) 또는 `pip install python-dotenv`(venv 사용시)
4. 프로젝트 settings.py 파일에서 `SECRET_KEY` 변수를 다음과 같이 수정:
	```python
	import os
	from dotenv import load_dotenv
	
	load_dotenv()
	
	SECRET_KEY = os.getenv('SECRET_KEY')
	```

<br>

---
# 참고자료
- Chat GPT를 통해 가물가물하던 기억을 상기
- https://dev.to/emma_donery/python-dotenv-keep-your-secrets-safe-4ocn

[^1]: