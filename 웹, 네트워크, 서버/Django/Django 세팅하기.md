---
date: 2023-03-20, Mon
topics: 알고리즘 공부 방법/순서, 
tags: 덕몽어스, 구스구스덕, 파이썬, 장고, python, django
---
# [Django](https://drive.google.com/file/d/18XG3q4SAdsDTpN1VyvDfFKO7u2ZMTaxg/view)

> "회사에 들어가서 실력을 키우려면 베이스가 있어야 한다."

## 장고 세팅
```json
{
	...
	
	// Django - MULTICAMPUS setting
	"files.associations": {
		"**/*.html": "html",
			"**/templates/**/*.html": "django-html",
		"**/templates/**/*": "django-txt",
		"**/requirements{/**,*}.{txt,in}": "pip-requirements"
	},
	"emmet.includeLanguages": {
		"django-html": "html"
	}

	...

}
```

## 가상환경

```bash
# 1. 가상환경 생성(가상환경 이름 -> venv)
python -m venv {가상환경 이름}

# 2. 가상환경 활성화
## Windows
source venv/Scripts/activate
## MacOS, Linux
source venv/bin/activate

# 2-1. 패키지 목록 확인
pip list

# 2-2. 환경 종료
deactivate

# 3. django 설치(3.2.18 버전 설치)
pip install django=={version}

# 4. 의존성 파일 생성
pip freeze > requirements.txt

# 4-1. 의존성 파일 목록 전체설치
pip install -r requirements.txt
```

## django 프로젝트 생성
```bash
django-admin startproject {프로젝트명} .

# 출력
zsh: command not found: django-admin

# 대안
python -m django startproject firstpjt .

# 출력
/Users/thebjko/.pyenv/versions/3.11.1/bin/python: No module named django

```
### 상황 및 해결
가상환경이 설치된 디렉토리명을 바꿨었다. (이게 원인인가?) 다시 확인해보니 django가 설치되어 있지 않다고 한다. 다시 설치하니 정상적으로 프로젝트가 생성되었다.
`pip freeze` 해보니 `pipenv`가 설치되어있다? 왜이렇지?

## django 서버 실행
```zsh
python manage.py runserver
```

[gitignore 만들어주는 사이트](https://www.toptal.com/developers/gitignore/)

## django shell-plus
1. 패키지 설치
```zsh
pip install ipyhton
pip install django_extensions
```

2. `django-extensions` app 추가
```python
# settings.py
# INSTALLED_APPS 리스트에 django_extensions 추가
INSTALLED_APPS = [
  # 생략 ...
  "django_extensions",
]
```

3. shell 진입
```zsh
python manage.py shell_plus
```