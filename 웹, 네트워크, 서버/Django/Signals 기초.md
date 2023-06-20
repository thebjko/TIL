---
created_at : 2023-06-15, Thu
유효기록일 : 2023-06-15, Thu
topics : 
context : 
tags : django signal
related : 
---
# Signals 기초
어떤 동작(action)이 실행되었을 때, 지정된 발신자(*senders*)에서 수신자(*receivers*)에게 동작이 실행되었음을 알려주는 기능. 여러 개의 다른 코드가 한 이벤트에 의해 촉발되어야 할 때 특히 유용하다.

```python
from django.apps import AppConfig
from django.core.signals import setting_changed


def my_callback(sender, **kwargs):
    print("Setting changed!")


class MyAppConfig(AppConfig):
    ...

    def ready(self):
        setting_changed.connect(my_callback)
```
`AppConfig.read`에서 `setting_changed.connect` 메서드로 `my_callback` 함수를 연결한다. 레지스트리가 채워졌을 때(서버가 구동 시작을 마치고 어플리케이션이 완전히 로드되었을 때) 연결된 `my_callback` 함수를 호출한다.[^1]

```python
from django.apps import AppConfig
from django.db.models.signals import pre_save


class RockNRollConfig(AppConfig):
    # ...

    def ready(self):
        # importing model classes
        from .models import MyModel  # or...

        MyModel = self.get_model("MyModel")

        # registering signals with the model's string label
        pre_save.connect(receiver, sender="app_label.MyModel")
```


> [!Warning]  
> 콤포넌트의 변경이 다른 콤포넌트들의 변경을 요구하는 내부 의존성을 줄이기 위한 느슨한 결합(Loose Coupling)[^2]의 모양을 갖게 하지만 코드가 이해, 변경, 디버그 하기 어려워질 수 있기 때문에, **가능하다면 시그널을 사용하는 대신 해당 메서드 내에서 다른 메서드를 직접 호출**할 것.

## Listening to signals
수신자 함수를 `Signal.connect()` 메서드를 사용해 등록한다. 시그널이 발생할 때 수신자 함수가 등록된 순서대로 호출된다.

#### `Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)`[\[source\]](https://docs.djangoproject.com/en/4.2/_modules/django/dispatch/dispatcher/#Signal.connect)
##### Parameters
- `receiver` : 시그널이 발생할 때 호출될 함수. receiver 데코레이터를 달고 있는 수신자 함수
- `sender` : 어떤 Model에서 발생하는 시그널을 사용할 것인가?
- `weak` : 인스턴스가 생성되어 유지되고 있는 메서드가 아닌 로컬 함수를 수신자 함수로 지정했을 때, 가비지 콜렉트 당할 수 있는데, 이것을 방지하기 위해 `weak` 인자에 `False`를 전달하라.
- `dispatch_uid` : 시그널 중복을 방지하기 위해 고유 값을 전달.

### 수신자 함수
```python
def my_callback(sender, **kwargs):
    print("Request finished!")
```
모든 수신자 함수는 `sender`와  `kwargs`를 인자로 받아야 한다. [`request_finished`](https://docs.djangoproject.com/en/4.2/ref/signals/#request-finished)는 `sender` 이외에 다른 인수를 전달하지 않기 때문이다. 

그렇다고 해서 `my_callback(sender)`라고만 하면 Django는 에러를 발생시킨다. 어느 시점에 다른 인자가 추가될 수 있기 때문이라고 한다.[^6]

### 수신자 함수 연결하기
두가지 방법이 있다.

#### Manual connect route:
```python
from django.core.signals import request_finished

request_finished.connect(my_callback)
```

#### `receiver(signal, **kwargs)`데코레이터 사용
```python
from django.core.signals import request_finished
from django.dispatch import receiver


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
```
인수로 신호 인스턴스를 전달한다. `request_finished`에 의해 매 요청이 완료되면 신호가 발생해 `my_callback` 함수를 호출하도록 되어있다.


다음은 `receiver` 데코레이터의 소스코드이다:
```python
def receiver(signal, **kwargs):
    """
    A decorator for connecting receivers to signals. Used by passing in the
    signal (or list of signals) and keyword arguments to connect::

        @receiver(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs):
            ...

        @receiver([post_save, post_delete], sender=MyModel)
        def signals_receiver(sender, **kwargs):
            ...
    """

    def _decorator(func):
        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(func, **kwargs)
        else:
            signal.connect(func, **kwargs)
        return func

    return _decorator
```
주석에서 볼 수 있는 것 처럼 여러가지 신호에 반응하게 할 수 있다.

📝 시그널을 다루는 코드와 등록하는 코드는 어디든 존재할 수 있지만, 임포트시 발생하는 부작용을 최소화하기 위해 어플리케이션의 root 모듈이나 models 모듈에 둘 것을 권장한다.  
**In practice**, 시그널 핸들러(시그널이 발생할 때 실행되는 콜백 함수)는 주로 어플리케이션의 signals 서브모듈에 위치시키고, `@receiver` 데코레이터를 사용해 만들어진 시그널 리시버는 어플리케이션 configuration class[^3]의 `ready` 메서드 안에서 연결된다(apps.py). `receiver` 데코레이터를 사용하는 경우 아래와 같이 signals 서브모듈을 임포트하면 암시적으로 시그널 핸들러와 연결된다.

apps.py
```python
from django.apps import AppConfig
from django.core.signals import request_finished


class MyAppConfig(AppConfig):
    ...

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals

        # Explicitly connect a signal handler.
        request_finished.connect(signals.my_callback)
```

예를 들어, 아래와 같이 `Post`, `Review`가 삭제되었을 때 실행될 시그널 핸들러들을 signals.py에 배치시킨다.
```python
# signals.py
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db.models.signals import pre_delete

from .models import Post, Review


@receiver(pre_delete, sender=Post)
def delete_post_images(sender, instance, **kwargs):
    instance.review_set.all().delete()

    for post_image in instance.post_images.all():
        default_storage.delete(post_image.image.name)
        post_image.delete()


@receiver(pre_delete, sender=Review)
def delete_reivew_images(sender, instance, **kwargs):
    for review_image in instance.review_images.all():
        default_storage.delete(review_image.image.name)
        review_image.delete()

```

각 모델에서 발생하는 `pre_delete` 시그널을 받아 실행된다. `connect` 메서드로 연결되지 않았지만 해당 핸들러들을 실행시킬 수 있는 이유는, `models.Model`의 `delete` 메서드에서 `Collector` 클래스의 `delete` 메서드를 실행하는데, 아래에서 볼 수 있듯, 여기서 `pre_delete.send` 메서드로 신호를 보내기 때문이다. 

`pre_delete` 메서드는 `ModelSignal` 클래스의 인스턴스이다. 

```python
# django.db.models.deletion
class Collection:
	...
	
	def delete(self):
		...
	
	     with transaction.atomic(using=self.using, savepoint=False):
	        # send pre_delete signals
	        for model, obj in self.instances_with_model():
	            if not model._meta.auto_created:
	                signals.pre_delete.send(
	                    sender=model,
	                    instance=obj,
	                    using=self.using,
	                    origin=self.origin,
	                )
		
		...
    
    ...
    
```

즉, 시그널 핸들러 함수를 호출하려면 우선 connect로 등록 후 send로 신호를 보내거나, `receiver` 데코레이터를 사용해야 한다.

```python
from django.db import models
from django.dispatch import receiver

from .signals import demo_signal


class Demo(models.Model):
    demo = models.CharField("demo", max_length=50)

    def send_signal(self):
        demo_signal.send()
        print('signal sent')

    def connect_receiver(self):
        demo_signal.connect(signal_handler, sender=self)


def signal_handler(**kwargs):   # 반드시 **kwargs를 인자로 받아야 한다.
    print('signal handled')
```

^61230c

위 모델에서 `connect_receiver` 메서드를 실행하기 전 아무리 `send_signal` 메서드를 호출해도 `signal_handler`가 호출되지 않는다. 하지만 아래와 같이 `receiver` 데코레이터를 사용하면
```python
@receiver(demo_signal)
def signal_handler(**kwargs):
	print('signal handled')
	
```
같은 결과를 얻을 수 있다.

```python
In [1]: demo = Demo.objects.create(demo='demo')

In [2]: demo
Out[2]: <Demo: Demo object (2)>

In [3]: demo.send_signal()
signal sent

In [4]: demo.connect_receiver()

In [5]: demo.send_signal()
signal handled
signal sent
```

`signal handled`가 먼저 출력됨을 확인하자.

📝 또, `AppConfig.ready` 메서드는 테스트시 여러 번 호출될 수 있기 때문에, `dispatch_uid`를 사용해 신호 중복을 방지하는게 좋다.

### 특정 발신자 지정하기
어떤 모델 인스턴스가 저장 또는 삭제되었을 때, 그 특정 모델이 발생시키는 신호만 수신하도록 아래와 같이 `sender` 인자에 모델을 전달할 수 있다
```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import MyModel


@receiver(pre_save, sender=MyModel)
def my_handler(sender, **kwargs):
    ...
```

`pre_save` 시그널(메서드)은 어떤 인스턴스가 저장되려 할 때, 즉 `save` 메서드가 호출되는 시점, 하지만 아직 저장되지는 않은 시점에 발생해 리시버를 통해 등록된 시그널 핸들러를 호출한다. `sender`, `instance`, `raw`, `using`, `update_fields`를 인자로 받는다.[^4] 여기서 `MyModel` 클래스를 `sender`로 전달하고 있고, 위 `receiver` 데코레이터를 통해 `pre_save` 메서드에 전달한다. 해당 클래스 인스턴스의 `save` 메서드가 실행될 때 신호가 발생한다.

[[Signals 기초#^61230c|위 예]]를 다시 보자.
```python
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

from .signals import demo_signal

# Create your models here.
class Demo(models.Model):
    demo = models.CharField("demo", max_length=50)

    def send_signal(self):
        demo_signal.send(sender=self.__class__)
        print('signal sent')

class Dummy(models.Model):
    dummy = models.CharField('dummy', max_length=50)

    def send_signal(self):
        demo_signal.send(sender=self.__class__)
        print('dummy signal sent')


@receiver(demo_signal, sender=Demo)
def signal_handler(**kwargs):
    print('demo signal handled')

@receiver(demo_signal, sender=Dummy)
def signal_handler(**kwargs):
    print('dummy signal handled')
```
위와 같이 각 핸들러 함수에 `sender` 모델을 전달하고, `send` 메서드에, 각 인스턴스의 클래스를 전달하면, 원하는 모델에서 원하는 핸들러를 호출할 수 있다.
```python
In [1]: dummy = Dummy.objects.first()

In [2]: dummy.send_signal()
dummy signal handled
dummy signal sent

In [3]: demo = Demo.objects.first()

In [4]: demo.send_signal()
demo signal handled
signal sent
```

어떤 시그널이 어떤 `sender`를 받는지는 공식 문서를 참고하자.[^5]

### 시그널 중복 방지하기
특정 환경에서 수신자와 발신자를 연결하는 코드가 여러번 실행될 수 있다. 이 경우 신호가 발생될 때 시그널 핸들러 함수가 여러번 실행된다. 예를 들어 위에서 언급한 `AppConfig.ready` 메서드가 있다. 좀 더 일반적으로 말하면, 시그널이 정의된 모듈을 임포트 할 때마다 실행되는데, 임포트 되는 만큼 시그널 등록(signal registration) 코드가 실행되기 때문이다.

예를 들어, 시그널이 발생할 때마다 이메일을 발송하는 로직이 있다면 문제가 될 수 있다. 이를 방지하기 위해 `dispatch_uid`를 사용한다. 문자열 또는 hashable 객체면 충분하다. 여러번 실행되더라도 같은 `dispatch_uid` 값을 갖는 신호는 한번만 처리된다.

```python
from django.core.signals import request_finished

request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")
```

<br>

## 시그널 정의하기/보내기
시그널 커스텀하기

### 시그널 정의하기
모든 시그널은 `django.dispatch.Signal`의 인스턴스이다. [\[source\]](https://docs.djangoproject.com/en/4.2/_modules/django/dispatch/dispatcher/#Signal)

```python
import django.dispatch

pizza_done = django.dispatch.Signal()
```

### 시그널 보내기

두 가지 방법이 있다.

- `Signal.send(sender, **kwargs)` : 
- `Signal.send_robust(sender, **kwargs)` : 

둘 다 receiver와 response 튜플로 이루어진 리스트를 반환한다(`[(receiver, response), ... ]`). 

`kwargs`로 전달된 인수는 핸들러 함수 내에서 사용할 수 있다.

`send`는 에러를 지나가게 둔다(propagate; pass on, transmit). 
`send_robust`는 에러를 캐치 → 모든 수신자가 신호를 받았음을 확실히 한다. 에러가 발생하면 에러 인스턴스가 response로 반환된다.
traceback은 `__traceback__` 속성에 있다.

<br>

## 연결 종료하기
`Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)`
종료시 `True`를 반환하지만 `sender`가 lazy reference로 전달된 경우(`<app label>.<model>`) `None`을 반환한다. 연결시 `dispatch_uid`를 사용한 경우 `None`을 반환한다.

<br>

---
# 참고자료
- [Django Doc 4.2 on Signals](https://docs.djangoproject.com/en/4.2/topics/signals/)
- [스케줄러 초기화](https://codingdog.tistory.com/entry/django-app-config-ready-%ED%95%9C-%EB%B2%88%EB%A7%8C-%EC%8B%A4%ED%96%89%EB%90%98%EA%B2%8C-%ED%95%98%EB%A0%A4%EB%A9%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%ED%95%A0%EA%B9%8C%EC%9A%94)
- [`AppConfig.read()` 활용하기](https://velog.io/@kjyeon1101/Django-%EC%84%9C%EB%B2%84-%EC%8B%9C%EC%9E%91%ED%95%98%EC%9E%90%EB%A7%88%EC%9E%90-%EC%A3%BC%EA%B8%B0%EC%A0%81%EC%9C%BC%EB%A1%9C-%EB%B6%88%EB%9F%AC%EC%98%A8-%EB%8D%B0%EC%9D%B4%ED%84%B0-DB%EC%97%90-%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0-2)
- [Django Doc 4.2 on Application Configuration - Methods](https://docs.djangoproject.com/en/4.2/ref/applications/#methods)
- [Django Doc 4.2 on Custom Managers](https://docs.djangoproject.com/en/4.2/topics/db/managers/#custom-managers)
- [Django Doc 4.2 on Overriding predefined model methods](https://docs.djangoproject.com/en/4.2/topics/db/models/#overriding-predefined-model-methods)
- [암시적 - 쓰레기를 줄이는 타입 설계 가이드](https://dataonair.or.kr/db-tech-reference/d-lounge/technical-data/?mod=document&uid=235820#:~:text=%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9D%98%20%EB%B0%98%EB%8C%80%EB%A7%90%EC%9D%80%20'%EC%95%94%EC%8B%9C,%EC%9C%BC%EB%A1%9C%20%ED%91%9C%ED%98%84%ED%95%A0%20%EB%95%8C%20%EC%93%B0%EB%8A%94%20%EB%A7%90%EC%9D%B4%EB%8B%A4.)




[^1]: [`AppConfig.ready()`](https://docs.djangoproject.com/en/4.2/ref/applications/#methods)
[^2]: [느슨한 결합(Loose Coupling)](https://swk3169.tistory.com/185)
[^3]: [Django Doc 4.2 on Configuring application](https://docs.djangoproject.com/en/4.2/ref/applications/#configuring-applications-ref)
[^4]: [Django Doc 4.2 on `pre_save`](https://docs.djangoproject.com/en/4.2/ref/signals/#pre-save)
[^5]: [Django Doc 4.2 on Signals](https://docs.djangoproject.com/en/4.2/topics/signals/)
[^6]: [`kwargs` on Receiver](https://stackoverflow.com/questions/20332551/how-django-signal-receiver-should-handle-errors)
