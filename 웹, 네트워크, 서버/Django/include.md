---
date:  2023-03-23, Thu
subjects: django, include, urls
context: 
---
# `include()`
> 다른 URL들을 참조할 수 있도록 돕는 함수

앱이 많아질 경우 프로젝트 레벨 urls.py에서 모든 URL들을 관리하기 번거로워진다. 이 때 각 앱에 해당하는 URL들을 앱 레벨 urls.py로 분배하고, 프로젝트 레벨 urls.py에서 `include()` 함수를 사용해 관리한다.

## Import
```python
from django.urls import path, include
```
django의 urls 모듈에서 불러온다.

## Workflow
프로젝트 레벨 urls.py:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('throw_and_catch.urls')),
]
```
추가하고자 하는 어플리케이션의 urls.py 파일을 불러오기 위해 `include()`함수의 인자로 `{어플리케이션 이름}.{파일 이름(확장자 제외)}`를 전달한다. 

어플리케이션 레벨 urls.py 파일을 만들고, `django.urls`에서 `path` 모듈을 불러오고, views.py 파일의 함수들을 사용해야 하므로 현재 디렉토리(어플리케이션 레벨)에서 views.py를 불러온다
```python
from django.urls import path
from . import views
```

`urlspatterns` 라는 리스트를 만든다. 리스트의 이름은 반드시 `urlspatterns`여야 한다. 그 안에 `path()` 함수로 아래와 같이 추가한다
```python
urlpatterns = [
	path('throw/', views.throw),
	path('catch/', views.catch),
]
```
`path()` 함수에 첫 번째로 주어지는 인자 값은 슬래시`/` 로 시작하지 않아도 된다. 하지만 html 문서에 하드코딩된 URL 주소는 슬래시로 시작해야 한다. 그렇지 않으면 경로가 추가되는 식으로 작동한다.

예를 들어, `/123/456/`에서 `567/`로 코딩된 a 태그는 `/123/456/567/`로 이동하지만, `/567/`로 코딩된 태그는 `/567/`로 이동한다.