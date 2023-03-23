---
date:  2023-03-23, Thu
subjects: django, url naming,
---
> [include](include.md)와 같이 보기
# URL Naming
URL이 바뀔 때마다 URL이 사용된 곳을 일일이 찾아가며 수정해야한다면 번거로운 일일 것이다. 이를 막기 위해 Django는 URL을 동적으로 관리할 수 있게 해주는 Naming 기능을 제공한다.

다음은 어플리케이션 레벨 urls.py이다.  

throw_and_catch/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
	path('throw/', views.throw, name="throw"),
	path('catch/', views.catch, name="catch"),
]
```

`path()` 함수 `name` 인자에 이름을 지정했다. 이 값을 template에서 `url` 태그에 사용할 수 있다.

throw_and_catch/throw.html
```html
{% extends 'base.html' %}

{% block title %}
Throw
{% endblock title %}

{% block content %}
<form action="{% url 'catch' %}">
  <label for="message">Message : </label>
  <input type="text" name="message" placeholder="내용을 입력하세요">
  <button type="submit" class="btn btn-info">Info</button>
</form>
{% endblock content %}
```

throw_and_catch/catch.html
```html
{% extends 'base.html' %}

{% block title %}
Catch
{% endblock title %}

{% block content %}
<h1>{{ data }}</h1>
<a href="{% url 'throw' %}">
  <button type="button" class="btn btn-link">뒤로가기</button>
</a>
{% endblock content %}
```

그런데 프로젝트가 커지다 보면 이 이름들이 중복되는 경우가 있다고 한다. 예를 들어 index.html 파일 같은 경우 각 어플리케이션마다 하나씩 있을 수 있다. 그럴때 일일이 다른 이름으로 지정해 주는 방법도 있지만 아래와 같이 `app_name`을 지정해 해결할 수 있다.

```python
from django.urls import path
from . import views

app_name = "throw_and_catch"
urlpatterns = [
	path('throw/', views.throw, name="throw"),
	path('catch/', views.catch, name="catch"),
]

```
`app_name` 변수에 어플리케이션 별칭을 정해 할당했다. 어플리케이션 별칭이 지정되면 템플릿 파일의 `url` 태그도 아래와 같이 view 함수 앞에 어플리케이션 별칭을 지정하는 식으로 변경해야 한다.

throw_and_catch/throw.html
```python
{% extends 'base.html' %}

{% block title %}
Throw
{% endblock title %}

{% block content %}
<form action="{% url 'throw_and_catch:catch' %}">
  <label for="message">Message : </label>
  <input type="text" name="message" placeholder="내용을 입력하세요">
  <button type="submit" class="btn btn-info">Info</button>
</form>
{% endblock content %}
```

throw_and_catch/catch.html
```python
{% extends 'base.html' %}

{% block title %}
Catch
{% endblock title %}

{% block content %}
<h1>{{ data }}</h1>
<a href="{% url 'throw_and_catch:throw' %}">
  <button type="button" class="btn btn-link">뒤로가기</button>
</a>
{% endblock content %}
```