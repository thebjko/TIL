---
created_at : 2023-06-07, Wed
유효기록일 : 2023-06-07, Wed
topics : 
context : celery django
tags : python 
related : 
---
# Dunder init file

`__init__.py` 파일은 Python의 특별한 파일로서, 그것이 위치한 디렉토리를 Python 패키지로 표시하는 역할을 합니다. 이 파일이 있는 디렉토리는 Python에서 임포트할 수 있는 모듈 또는 패키지로 인식됩니다.

`__init__.py` 파일 안에 `celery = Celery('proj')`와 같은 코드를 삽입하면, 다른 Python 모듈에서 `from proj import celery`와 같이 이 celery 객체를 바로 임포트할 수 있습니다.

`__init__.py` 파일에서 `from .celery import app as celery_app` 구문은 현재 패키지에서 celery 모듈을 찾고, 그 모듈 안의 app 객체를 `celery_app`로 임포트하라는 의미입니다. 이렇게 하면, 다른 Python 모듈에서 Django 프로젝트의 Celery 애플리케이션에 쉽게 접근할 수 있습니다.

마지막 줄의 `__all__ = ('celery_app',)` 코드는 이 모듈에서 어떤 이름들이 임포트 가능한지를 지정하는 리스트입니다. 이 경우에는 celery_app만 임포트 가능하도록 설정되었습니다. `__all__`을 설정하면, 외부에서 이 모듈을 임포트할 때 어떤 이름들이 이 모듈의 공개 인터페이스로 볼 것인지를 명확하게 할 수 있습니다.


---
# 참고자료
- ChatGPT


[^1]: 
