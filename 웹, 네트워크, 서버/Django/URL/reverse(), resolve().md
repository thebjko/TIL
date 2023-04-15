---
created_at : <% tp.file.creation_date("YYYY-MM-DD, ddd") %>
유효기록일 : <% tp.date.now("YYYY-MM-DD, ddd") %>
topics : reverse, resolve
context : v3.2
tags : python/django/url reverse, resolve
related : 
---
# `reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)`

URL이 필요할 때, name을 사용할 수 없을 때, reverse함수를 통해 URL 패턴을 생성한다.
```python
from django.urls import reverse

reverse('my_app:my_view', args=(1,))
# reverse(views.my_view, arges=(1,))   # viewname 사용시
# reverse('my_app:my_view', kwargs={'pk': 1})   # kwargs 사용시
```
kwargs는 args와 동시 사용 불가.  

<br>

args는 아래와 같이 my_view에서 variable routing을 사용할 때 인수로 제공한다.
```python
app_name = 'my_app'
urlpatterns = [
	path('my_app/<int:pk>/', views.my_view, name='my_view'),
]
```

[[URL Naming]]을 사용하면 많은 경우 `reverse()`를 사용할 필요가 없는 듯 한데, 다만 url 템플릿 태가와 같은 기능이 필요할 때가 있는 듯하다. 예를 들어 url path를 context로 넘겨줄 수 있는데, `{% url 'url_name' as my_url %}`처럼 템플릿에 작성하지 않고 사용할 수 있다(`{'my_url': reverse('url_name')}`). 이 때 url을 템플릿으로 보내기 전에 view 함수에서 전처리 할 수 있다는 이점이 있다.

<br>

# `resolve(path, urlconf=None)`
`reverse()`와 반대되는 기능을 한다. path를 제공하면 ResolverMatch 객체를 반환한다. 매치 되는 뷰가 없다면 Resolver404 예외를 발생시킨다.

아직 사용할 일이 없어 와닫지 않는 내용이 많아 나중에 돌아오기로 한다.

<br>

---
# 참고자료
- ChatGPT
- https://ugaemi.com/django/Django-reverse-and-resolve/
- https://docs.djangoproject.com/en/3.2/ref/urlresolvers/#reverse
- https://docs.djangoproject.com/en/3.2/ref/urlresolvers/#resolve

[^1]: