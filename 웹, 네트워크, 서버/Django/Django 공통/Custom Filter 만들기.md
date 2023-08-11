---
created_at : 2023-04-17, Mon
유효기록일 : 2023-04-17, Mon
topics : Custom Tag
context : 
tags : python/django/template_language/customization
related : 
---
# Custom Filter 만들기
1. 어플리케이션/templatetags 디렉토리에 `__init__.py` 파일과 커스텀 템플릿 태그를 만들 파이썬 파일 하나를 만든다. 여기서는 `articles_extras.py`를 만들었다.
2. 커스텀 템플릿 태그를 사용할 템플릿 상단에 템플릿 태그를 담고 있는 파일을 load한다. `{% load articles_extras %}`
3. `template.Library()` 인스턴스를 만든다.
	```python
	from django import template
	
	register = template.Library()
	```
4. 함수를 작성한다. 함수는 2가지 인수를 받을 수 있다. 필터를 다음과 같이 사용한다면: `{{ value|filter:arg}}`, filter 함수는 value와 arg를 인수로 받는다는 뜻이다. 아래와 같이 작성했다.
	```python
	def likes_this(user, query):
	    return query.like_users.filter(pk=user.pk).exists()
	```
5. 커스텀 필터를 등록한다. 다음과 같은 방법이 있다.
	```python
	# 1. register의 filter 메서드
	register.filter('템플릿에서 사용할 이름', 작성한 함수)
	register.filter('likes_this', likes_this)
	
	# 2. 데코레이터 사용
	@register.filter(name='cut')
	def cut(value, arg):
	    return value.replace(arg, '')
	
	@register.filter
	def lower(value):
	    return value.lower()
	
	@register.filter(name='likes_this')
	def likes_this(user, query):
	    return query.like_users.filter(pk=user.pk).exists()
	```
	name 인자에 아무런 값도 제공하지 않으면, 함수 이름을 필터 이름으로 사용한다.

<br>

## 용례
2023 04 17 실습 MTM articles/detail.html
```django
{% extends "base.html" %}
{% load articles_extras %}

{% block content %}
  <div>
    ...
    <form action="{% url 'articles:like_article' article.pk %}" method="post">
      {% csrf_token %}
      {% if user|likes_this:article %}
      <input type="submit" value="좋아요 취소">
      {% else %}
      <input type="submit" value="좋아요">
      {% endif %}
    </form>
  </div>
  <hr>
  ...
  {% for comment in comments %}
  <div>
    ...
    <form action="{% url 'articles:like_comment' article.pk comment.pk %}" method="post">
      {% csrf_token %}
      {% comment %} {% if user in comment.like_users.all %} {% endcomment %}
      {% if user|likes_this:comment %}
      <input type="submit" value="좋아요 취소">
      {% else %}
      <input type="submit" value="좋아요">
      {% endif %}
    </form>
  </div>
  {% endfor %}
...
{% endblock content %}
```

<br>

---
# 참고자료
- https://realpython.com/django-template-custoom-tags-filters/#writing-django-template-custom-filters
- https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/

[^1]: