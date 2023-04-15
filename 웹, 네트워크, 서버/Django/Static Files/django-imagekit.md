---
created_at : 2023-04-15, Sat
유효기록일 : 2023-04-15, Sat
topics : 
context : 인스타그램 클론코딩
tags : python/django/package image
related : 
---
# django-imagekit
📝 이미지를 처리하고 변환하는 기능을 제공하는 Django 패키지

1. 설치
	```
	pip(pipenv) install Pillow
	pip(pipenv) install django-imagekit
	```

2. 이미지 모델 생성
	```python
	from django.db import models
	from imagekit.models import ImageSpecField
	from imagekit.processors import ResizeToFill, Adjust
	
	class MyImage(models.Model):
	    image = models.ImageField(upload_to='myimages')
	    thumbnail = ImageSpecField(
	        source='image',
	        processors=[ResizeToFill(100, 100)],
	        format='JPEG',
	        options={'quality': 90}
	    )
	    adjusted = ImageSpecField(
	        source='image',
	        processors=[Adjust(contrast=1.2, sharpness=1.1)],
	        format='JPEG',
	        options={'quality': 80}
	    )
	
	```

3. `SmartCrop` : 중심에서 정사각형 썸네일 생성하는 프로세서
	```python
	from imagekit.models import ImageSpecField
	from imagekit.processors import SmartCrop
	from django.db import models
	
	class MyModel(models.Model):
	    image = models.ImageField(upload_to='images')
	    thumbnail = ImageSpecField(
	        source='image',
	        processors=[SmartCrop(300, 300)],   # 300x300 사이즈 썸네일 생성
	        format='JPEG',
	        options={'quality': 90}
	    )
	```

<br>

---
# 참고자료
- ChatGPT
- https://pypi.org/project/django-imagekit/

[^1]: