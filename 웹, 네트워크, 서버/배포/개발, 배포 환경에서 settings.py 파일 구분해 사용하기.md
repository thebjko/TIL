---
created_at : 2023-05-08, Mon
유효기록일 : 2023-05-08, Mon
topics : 
context : 배포
tags : python/django/settings deploy
related : settings.py
---
# 개발, 배포 환경에서 settings.py 파일 구분해 사용하기

1. `__init__.py` 파일이 들어있는 setting 폴더 만들기
2. dev.py, prod.py, base.py

dev.py, prod.py 에 필요한 정보들을 가져오고 기존 settings.py(base.py) 파일에서 모든 정보들을 불러온다.
```python
from decouple import config   # 여기선 환경 변수를 사용하기 위해 decouple 패키지를 사용한다
from .base import *

SECRET_KEY = config('SECRET_KEY')
DEBUG = TRUE   # False for prod.py
ALLOWED_HOSTS = []
```

3. base.py에서 `BASE_DIR`에 `.parent`를 하나 더 붙인다.
```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

---
다음 단계부터는 두개의 브랜치를 두고 사용할 수 있다. 예를 들어 main 브랜치를 개발용으로 사용할 때 `'config.settings.dev'`를 사용하고, production 브랜치를 따로 마련해 `'config.settings.prod'`를 적어두는 식이다. 수정이 될 수 도 있는 settings.py를 두개 두는 것보다 훨씬 안전한 방법인 것 같다.

4. manage.py 파일 수정
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{프로젝트 이름}.settings.dev')
```
5. wsgi.py
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{프로젝트 이름}.settings.dev')
```
6. asgi.py
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{프로젝트 이름}.settings.dev')
```

<br>

---
# 참고자료
1. [How To Store Django Secret Keys In Development And Production](https://youtu.be/bPR3Q0BFFzw?t=570)
