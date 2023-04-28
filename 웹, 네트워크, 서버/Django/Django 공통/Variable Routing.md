---
date:  2023-03-23, Thu
subject: django, variable routing,
context: 
---
> [include()](include().md), [URL Naming](URL%20Naming.md)과 같이 보면 좋다.
# Variable Routing
URL에 입력한 값을 변수로 사용할 수 있게 해준다. 

## 이해
urls.py에 `path()` 함수에 들어가는 URL 인자에 `<path_converter:variabale_name>`과 같은 형식으로 작성한다.
```python
urlpatterns = [
    path('<int:num>/', views.number_print, name="print")
]
```
`<>` 안에 띄어쓰기가 있으면 안된다(`<int: num>` 안됨).

views.py:
```python
def print_number(request, num: int):
	context = {
	    "num": num,
	}
	return render(request, 'print_number/number_print.html', context)
```
위와 같이 전달하면

프로젝트 레벨 urls.py에 아래와 같이 작성되어 있으므로,
```python
urlpatterns = [
	... ,
    path('number-print/', include('print_number.urls')),
]
```

`/number-print/5`와 같은 URL에서 주어진 5를 템플릿에서 아래와 같이 사용할 수 있다.  

number_print.html
```html
{% block content %}
{{ num }}
{% endblock content %}
```

## 응용
> 요청의 흐름에 따라 작성합니다.

1. 프로젝트 레벨 URL 추가하기

	ProjectURL/urls.py
	```python
	urlpatterns = [
		... ,
	    path('calculate/', include('calculate.urls')),
	]
	```

2. 어플리케이션 레벨 URL 추가하기

	calculate/urls.py
	```python
	from django.urls import path
	from . import views

	app_name = "calc"
	urlpatterns = [
		path("index/", views.index, name="index"),
	    path("<int:num1>/<int:num2>", views.calculate, name="calculate"),
	]
	```

3. view 함수 작성하기

	views.py
	```python
	from django.shortcuts import render
	
	def calculate(request, num1: int = None, num2: int = None):
	context = {
		"data": {
			"더하기": num1 + num2,
			"빼기": num1 - num2,
			"곱하기": num1 * num2,
			"몫": num1 // num2 if num2 else "0으로 나눌 수 없습니다.",
		},
	}
	return render(request, 'calculate/calculate.html', context)
	```

4. 사용하기

	calculate/caluclate.html
	```html
	{% extends 'base.html' %}
	
	{% block title %}
	Calculate
	{% endblock title %}
	
	{% block content %}
	<div class="card" style="width: 300px;">
	  <div class="card-body">
	    <ul class="list-group list-group-flush">
	    {% for operation, value in data.items %}
	      <li class="list-group-item">{{ operation }} : {{ value }}</li>
	    {% endfor %}
	      <li class="list-group-item">
	        <a href="{% url 'calc:index' %}">뒤로가기</a>
	      </li>
	    </ul>
	  </div>
	</div>
	{% endblock content %}
	```
