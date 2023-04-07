---
created_at : <% tp.file.creation_date("YYYY-MM-DD, ddd") %>
유효기록일 : <% tp.date.now("YYYY-MM-DD, ddd") %>
topics : static files
context : 
tags : python/django
related : css, js, images, etc.
---
# BASE_DIR에서 static 디렉토리 사용하기

예를 들어, 다음과 같은 디렉토리 구조에 css 파일이 있다고 하자: `home/user/myproject/디렉토리이름/하위디렉토리/global.css`

settings.py
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "디렉토리이름"),
]
```

html
```django
{% load static %}

...

<link rel="stylesheet" type="text/css" href="{% static '하위디렉토리/global.css' %}" />   

```


---
# 참고자료
- https://stackoverflow.com/questions/35825114/django-where-to-store-global-static-files-and-templates

[^1]: