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

```python
INSTALLED_APPS += ['imagekit']
```

<br>

# 원본 파일도 같이 저장하기
Django-imagekit을 사용하여 이미지를 리사이즈하고, 원본 이미지와 리사이즈된 이미지 모두를 저장하려면, `imagekit.models.ProcessedImageField`를 사용하여 `spec_id` 매개변수를 지정해야 합니다. 이렇게하면, `spec_id` 매개변수를 사용하여 각 이미지 사양의 이름을 정의하고, 이미지 파일을 저장할 때 해당 이름으로 저장됩니다.

예를 들어, 다음과 같은 모델을 사용하여 `ResizeToFill`을 사용하여 원본 이미지와 리사이즈된 이미지 모두를 저장할 수 있습니다.

```python
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models

class MyModel(models.Model):
    original_image = models.ImageField(upload_to='original_images')
    resized_image = ProcessedImageField(upload_to='resized_images',
                                        processors=[ResizeToFill(300, 300)],
                                        format='JPEG',
                                        options={'quality': 90},
                                        spec_id='resized_image')

```

위의 코드에서 `resized_image` 필드는 `ProcessedImageField`로 정의되어 있습니다. 이 필드는 processors 매개변수를 사용하여 이미지를 리사이즈할 때 사용되는 `ResizeToFill` 프로세서를 지정합니다. 또한, format 및 options 매개변수를 사용하여 이미지 파일 형식 및 품질을 정의하고, `spec_id` 매개변수를 사용하여 이미지 사양의 이름을 정의합니다.

이렇게 하면, `resized_image` 필드에 이미지를 업로드하면 `original_image` 필드와 함께 두 이미지가 모두 저장됩니다. `original_image` 필드는 `upload_to='original_images'`를 사용하여 `MEDIA_ROOT/original_images`에 저장되고, `resized_image` 필드는 `upload_to='resized_images'`를 사용하여 `MEDIA_ROOT/resized_images/resized_image`에 저장됩니다.

하지만 위에서 설명한 방법으로 구현하면, 원본 이미지와 리사이즈된 이미지 모두를 저장하므로, Form에서 두 필드에 모두 입력해야 합니다. 이는 사용자 경험 측면에서 좋지 않을 수 있습니다.

따라서, 사용자가 한 번에 이미지를 업로드하면, 원본 이미지와 리사이즈된 이미지를 모두 저장하도록 하면 좋습니다. 이를 위해, `ImageSpecField`를 사용하여 리사이즈된 이미지를 생성하고, 이를 `ImageField`와 연결하여 모델에 저장할 수 있습니다.

예를 들어, 다음과 같은 모델을 사용하여 `ImageSpecField`와 `ImageField`를 함께 사용할 수 있습니다.
```python
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class MyModel(models.Model):
    image = models.ImageField(upload_to='images')
    resized_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(300, 300)],
                                   format='JPEG',
                                   options={'quality': 90})

```
위의 코드에서, `resized_image` 필드는 `ImageSpecField`로 정의되어 있습니다. 이 필드는 source 매개변수를 사용하여 리사이즈할 원본 이미지 필드를 지정하고, processors 매개변수를 사용하여 이미지를 리사이즈할 때 사용되는 `ResizeToFill` 프로세서를 지정합니다. 또한, format 및 options 매개변수를 사용하여 이미지 파일 형식 및 품질을 정의합니다.

이렇게 하면, `ImageField` 하나만 Form에 추가하면 됩니다. 사용자가 이미지를 업로드하면, `ImageField`에 저장된 원본 이미지와 함께 `ImageSpecField`에서 생성된 리사이즈된 이미지도 모두 저장됩니다. 따라서, 모델에서 두 개의 이미지 필드를 정의하고, Form에서 두 필드에 모두 입력할 필요가 없으므로, 사용자 경험이 개선됩니다.

<br>

# `pre_save` 신호 사용해 image가 업로드 될 때마다 resized_image에 저장되도록 구현하기

이미지가 저장될 때마다 실행되는 메서드를 사용하여 `resized_image` 필드를 구현하는 것은 가능하지만, 이는 비효율적일 수 있습니다. 이미지를 저장할 때마다 이미지를 재조정하는 것은 시간이 오래 걸리며, 서버의 부하를 증가시킬 수 있습니다.

대신, Django의 `pre_save` 신호를 사용하여 이미지를 저장하기 전에 `resized_image` 필드를 생성할 수 있습니다. 이 방법은 이미지를 한 번만 조정하고, 이후에는 필드를 다시 생성할 필요가 없으므로 효율적입니다.

```python
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class MyModel(models.Model):
    image = models.ImageField(upload_to='images')
    resized_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(300, 300)],
                                   format='JPEG',
                                   options={'quality': 90})

@receiver(pre_save, sender=MyModel)
def generate_resized_image(sender, instance, **kwargs):
    if instance.image:
        # 이미지가 업로드된 경우에만 실행
        # 여기서는 조건문을 빼도 무방하다.
        instance.resized_image.delete(save=False)
        instance.resized_image.create()

```

위 코드에서는 `pre_save` 신호를 사용하여 MyModel이 저장될 때마다 `generate_resized_image` 함수가 호출됩니다. 함수는 `instance.image`가 존재하는 경우에만 실행되며, 이미지가 업로드되지 않은 경우에는 `resized_image` 필드를 생성하지 않습니다.

함수는 먼저 `resized_image` 필드를 삭제하고, `create()` 메서드를 호출하여 `resized_image` 필드를 생성합니다. 이렇게 함으로써, 이미지를 한 번만 조정하고, 이후에는 필드를 다시 생성할 필요가 없으므로 효율적인 방법입니다.

`instance.resized_image.delete()` 메서드는 이전에 생성된 `resized_image` 파일을 삭제합니다. 이전 파일을 삭제하지 않고 그대로 둘 경우, 같은 파일 이름으로 새로운 `resized_image` 파일이 생성될 때 파일 이름이 중복되어 저장되는 문제가 발생할 수 있습니다.

이전 파일을 삭제하지 않고 그대로 두면, `resized_image` 필드가 수정될 때마다 파일 이름이 변경되는 것이 아니라, 같은 파일 이름으로 새로운 파일이 생성됩니다. 이러한 파일 중복으로 인해 디스크 공간이 낭비되고, 파일 시스템이 혼란스러워지는 문제가 발생할 수 있습니다.

따라서, `resized_image` 필드를 다시 생성하기 전에 이전에 생성된 resized_image 파일을 삭제해주는 것이 좋습니다. `save=False` 옵션을 사용하여 데이터베이스에 변경 내용을 저장하지 않고 파일만 삭제합니다. 이렇게 하면 파일이 삭제되고 `resized_image` 필드가 업데이트되어도 데이터베이스에는 변경 내용이 저장되지 않습니다.

<br>

# Appendix
## A. `spec_id`

`spec_id`는 `ImageSpecField`에서 사용할 수 있는 선택적인 매개변수입니다. 이 매개변수를 사용하면, `ImageSpecField`에서 생성된 이미지의 식별자를 지정할 수 있습니다.

기본적으로, `ImageSpecField`에서 생성된 이미지는 원본 이미지와 동일한 경로에 저장됩니다. 이 경우, `spec_id`는 필요하지 않습니다. 그러나, `spec_id`를 사용하여 생성된 이미지를 원본 이미지와 다른 경로에 저장하고, 이미지를 식별할 수 있습니다.

예를 들어, `spec_id`를 사용하여 다양한 크기의 이미지를 다른 경로에 저장하고, 이미지를 식별하는 방법을 보여드리겠습니다.

```python
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class MyModel(models.Model):
    image = models.ImageField(upload_to='images')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(100, 100)],
                               format='JPEG',
                               options={'quality': 90},
                               spec_id='thumbnail')
    medium = ImageSpecField(source='image',
                            processors=[ResizeToFill(300, 300)],
                            format='JPEG',
                            options={'quality': 90},
                            spec_id='medium')

```

위의 코드에서, `thumbnail` 필드와 `medium` 필드는 각각 `spec_id`를 사용하여 이미지를 다른 경로에 저장합니다. `thumbnail` 필드는 `spec_id`가 `'thumbnail'`인 이미지를 생성하고, `medium` 필드는 `spec_id`가 `'medium'`인 이미지를 생성합니다. 이렇게 하면, `ImageSpecField`에서 생성된 각 이미지는 원본 이미지와 다른 경로에 저장됩니다. 이러한 이미지는 다른 용도로 사용할 수 있으며, `spec_id`를 사용하여 해당 이미지를 식별할 수 있습니다.

따라서, `spec_id`는 선택적인 매개변수이며, `ImageSpecField`에서 생성된 이미지의 식별자를 지정할 때 사용됩니다. 이를 사용하면, 다양한 크기와 형식의 이미지를 생성하여 원본 이미지와 다른 경로에 저장하고, 해당 이미지를 식별할 수 있습니다.

<br>

# `resized_image`의 파일 이름
`ImageSpecField`를 사용하여 생성된 이미지 파일의 이름은 다음과 같은 패턴을 따릅니다.

```
<original_image_name>_<processor_name>_<option1>_<option2>_<...>.<format>
```

여기서 `<original_image_name>`은 원본 이미지 파일의 이름을 의미하며, `<processor_name>`은 사용된 `Processor`의 이름입니다. 위 코드에서는 `ResizeToFill` 프로세서를 사용하고 있으므로, `<processor_name>`은 `resize_to_fill`이 됩니다.

`<option>`은 사용된 `Processor`의 옵션을 나타냅니다. 위 코드에서는 `ResizeToFill` 프로세서의 `width`와 `height`를 각각 300으로 지정하고 있으므로, `<option>`은 `300x300`이 됩니다.

`<format>`은 생성된 이미지 파일의 확장자입니다. 위 코드에서는 JPEG를 사용하고 있으므로, `<format>`은 jpg가 됩니다.

예를 들어, 원본 이미지 파일의 이름이 `my_image.jpg`인 경우, `ResizeToFill` 프로세서를 사용하여 크기를 300x300으로 조정한 이미지 파일의 이름은 다음과 같이 됩니다.

```
my_image_resize_to_fill_300x300.jpg
```

<br>

---
# 참고자료
- ChatGPT
- https://pypi.org/project/django-imagekit/

[^1]: