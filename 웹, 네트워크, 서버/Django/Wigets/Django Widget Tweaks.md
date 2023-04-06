---
created_at : 2023-04-07, Fri
유효기록일 : 2023-04-07, Fri
topics : 위젯에 속성 추가하는 플러그인R
context : django widgets
tags : python/django/widget
related : 
---
# Django Widget Tweaks

## 사용법
1. 설치
	```zsh
	pip install django-widget-tweaks
	```

2. settings.py
	```python
	INSTALLED_APPS += [
		"widget_tweaks",
	]
	```

3. load and render
	```html
	{% load widget_tweaks %}
	
	...

	{% render_field form.name placeholder="Name" class+="form-control" %}

	...

	```

render_field 태그 안에서 지정한 속성이 html 요소에 적용된다. 지정하지 않은 요소는 기본값으로 설정된다.

---
# 참고자료
- [Pretty Printed 유튜브 채널](https://youtu.be/ynToND_xOAM) 
- [django-widget-tweaks 공식문서](https://pypi.org/project/django-widget-tweaks/)

[^1]: