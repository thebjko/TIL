---
date:  2023-03-21, Tue
subject: django
tags: django, python
context: Django 세팅하기
---
> [Django 세팅하기](Django%20%EC%84%B8%ED%8C%85%ED%95%98%EA%B8%B0.md) 이후에 진행되는 과정입니다.

# Django 프로젝트 시작하기

## 1. 프로젝트 생성
```zsh
django-admin startproject {프로젝트명}
```

## 2. 앱 생성
```zsh
python manage.py startapp {어플리케이션명(복수)}
```

## 3. 앱 등록하기
```python
# {프로젝트명}/settings.py
INSTALLED_APPS = [
	'{어플리케이션명}',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]
```

## 4. 데이터의 흐름에 따라 어플리케이션 작성하기
> 클라이언트 측으로부터 요청이 오면 `urls.py`가 요청을 라우팅하고, `views`로 전달, `views`는 `template`을 가져와 클라이언트에게 반환한다.

### 1. `urls.py`
```python
# {프로젝트명}/urls.py
from django.contrib import admin
from django.urls import path

from {어플리케이션명} import views   # {어플리케이션명}/views.py
urlpatterns = [
	path('admin/', admin.site.urls),
	path('{요청하려는 url}/', 가져오려는 콜백함수),
]
```
> 1. url 뒤에 `/`(슬래시)를 꼭 붙여야 한다.
> 2. `path` 함수의 인자로 콜백함수를 전달한다.

### 2. `views.py`
```python
# {어플리케이션명}/views.py
from django.shortcuts import render

def index(request):
	return render(request, '{가져오려는 템플릿 이름}')
```

### 3. `templates`
어플리케이션 디렉토리 안에 **`templates/{어플리케이션명}`** 으로 디렉토리를 생성하고, 템플릿을 저장한다. `templates` 이하부터 경로를 작성한다.
> `template`이 아니라 `templates`다. 꼭 이 이름으로 하는게 중요하다.

---

## 5. [이미지 사용하기](https://docs.djangoproject.com/en/3.2/howto/static-files/)
### `settings.py`
1. `INSTALLED_APPS`에 `django.contrib.staticfiles`가 추가되어 있는지 확인하기
2. `STATIC_URL` 변수명에 저장된 값 확인하기 (`/static/`)

### `index.html`
3. `index.html` 파일에 아래와 같이 추가하기
```python
{% load static %}
<img src="{% static '{어플리케이션명}/{파일명}' %}" alt="...">

```
4. `{어플리케이션명}/static/{어플리케이션명}` 경로에 이미지 파일 저장하기