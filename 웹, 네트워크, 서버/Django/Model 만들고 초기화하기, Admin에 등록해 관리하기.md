---
created : 2023-03-24, Fri
topics : model, migration, admin,
context : django, 
---
# 워크플로우
1. Model 만들기  
	models.py
	```python
	from django.db import models
	
	
	# Create your models here.
	class Todo(models.Model):
	    content = models.CharField(max_length=80)
	    completed = models.BooleanField(default=False)
	    priority = models.IntegerField(default=3)
	    created_at = models.DateField(auto_now_add=True)
	    deadline = models.DateField(null=True)
	
	    category = models.CharField(max_length=20)
	
	```

2. `python manage.py makemigrations` :  모델 설계도 업데이트
	- `migrations` 디렉토리에 `Migration` 클래스가 담긴 `py` 파일이 생성된다.
3. `python manage.py migrate` : 업데이트한 설계도 DB에 반영하기
	- `Applying todos.0001_initial... OK`와 같은 메세지들이 터미널에 출력된다.

## 기타
1. `python manage.py showmigrations`
	- 반영된 `migrations`를 확인하는 커맨드.
	- 앞에 `[X]` 표시가 뜬다면 잘 되었다는 뜻이다.
		- `migrate` 이후에 `[X]` 표시가 된다.
1. `python manage.py sqlmigrate application_name migration_file_number`
	- SQL 명령어로 번역된 `Migration` 파일이 터미널에 출력된다.
2. VSCode SQLite Viewer 확장 프로그램

## DB 초기화하기
migrations 파일들과 db.sqlite3 파일을 삭제한다.

# Admin
1. 생성하기
	- 첫 번째 migration 이후 아래의 명령을 입력해 관리자 계정을 만들 수 있다
	- `python manage.py createsuperuser`
2. /admin 페이지에서 로그인해 페이지들을 관리 할 수 있다.

## Model 등록하기
> Model을 등록한 후에 admin 페이지에서 관리할 수 있다.  

admin.py
```python
from django.contrib import admin
from .models import Todo

# admin site에 Todo를 register한다.
admin.site.register(Todo)
```