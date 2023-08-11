---
created_at : 2023-06-07, Wed
유효기록일 : 2023-06-07, Wed
topics : 
context : 
tags : celery django apply_async delay
related : 
---
# Learn Django Celery with RabbitMQ - Install and create new celery instance, Run a simple task Part 1

1. 브로커 선택 및 설치(RabbitMQ)

	- MacOS
		```
		brew install rabbitmq
		brew services start rabbitmq
		```
	
	- Ubuntu
		```
		sudo apt-get install rabbitmq-server
		sudo systemctl enable rabbitmq-server
		sudo systemctl start rabbitmq-server
		systemctl status rabbitmq-server 
		```
1. Install Celery
	```
	pip install celery
	```


project/celery.py
```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Django 프로젝트의 설정 모듈을 'celery' 프로그램의 기본 설정으로 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')

# 여기서 Celery 설정은 Django의 설정을 사용합니다.
# 'CELERY'라는 네임스페이스에서 시작하는 모든 구성 키를 사용합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱을 위한 Celery를 자동으로 로드합니다.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

```
나는 어플리케이션 레벨에 해당 파일을 만들었다.

app/tasks.py
```python
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.db.models import Count
from taggit.models import Tag

@shared_task
def remove_unused_tags():
	'''사용하지 않는 태그를 삭제하는 함수'''
    Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()


@shared_task
def add(x, y):
    return x + y

```

터미널 명령
```
brew services start rabbitmq
celery -A reviews worker --loglevel=INFO
# celery -A reviews worker -B -l info   # -B for embedding beat
# celery -A reviews beat -l info
```
출력
```
[2023-06-07 05:05:55,036: WARNING/MainProcess] No hostname was supplied. Reverting to default 'localhost'
 
 -------------- celery@Rocket-Launcher.local v5.3.0 (emerald-rush)
--- ***** ----- 
-- ******* ---- macOS-13.4-arm64-arm-64bit 2023-06-07 05:05:55
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         config:0x104d85d10
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . reviews.tasks.remove_unused_tags
```


rabbitmq를 꺼서 어떻게 달라지나 확인해보자
```
brew services stop rabbitmq
```

아래와 같은 에러메세지를 받는다.

```
[2023-06-07 05:06:48,362: ERROR/MainProcess] consumer: Cannot connect to amqp://guest:**@127.0.0.1:5672//: [Errno 61] Connection refused.
Trying again in 2.00 seconds... (1/100)

[2023-06-07 05:06:50,369: ERROR/MainProcess] consumer: Cannot connect to amqp://guest:**@127.0.0.1:5672//: [Errno 61] Connection refused.
Trying again in 4.00 seconds... (2/100)

[2023-06-07 05:06:54,374: ERROR/MainProcess] consumer: Cannot connect to amqp://guest:**@127.0.0.1:5672//: [Errno 61] Connection refused.
Trying again in 6.00 seconds... (3/100)
```

delay and 

```python
add.delay(4, 3)
<AsyncResult: 5fc596db-8e47-470f-a385-9de3d9ec192e>
```

아래와 같은 에러메세지도 받았다.
```
[2023-06-07 05:24:42,747: ERROR/MainProcess] Received unregistered task of type 'reviews.tasks.add'.
The message has been ignored and discarded.

Did you remember to import the module containing this task?
Or maybe you're using relative imports?

Please see
https://docs.celeryq.dev/en/latest/internals/protocol.html
for more information.

The full contents of the message body was:
'[[4, 3], {}, {"callbacks": null, "errbacks": null, "chain": null, "chord": null}]' (81b)

The full contents of the message headers:
{'lang': 'py', 'task': 'reviews.tasks.add', 'id': '5fc596db-8e47-470f-a385-9de3d9ec192e', 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'retries': 0, 'timelimit': [None, None], 'root_id': '5fc596db-8e47-470f-a385-9de3d9ec192e', 'parent_id': None, 'argsrepr': '(4, 3)', 'kwargsrepr': '{}', 'origin': 'gen18273@Rocket-Launcher.local', 'ignore_result': False, 'stamped_headers': None, 'stamps': {}}

The delivery info for this task is:
{'consumer_tag': 'None4', 'delivery_tag': 1, 'redelivered': False, 'exchange': '', 'routing_key': 'celery'}
Traceback (most recent call last):
  File "/Users/thebjko/.local/share/virtualenvs/Altudy-3WmqDoJv/lib/python3.11/site-packages/celery/worker/consumer/consumer.py", line 642, in on_task_received
    strategy = strategies[type_]
               ~~~~~~~~~~^^^^^^^
KeyError: 'reviews.tasks.add'
```

함수를 업데이트 하고 나서 셀러리 서버를 restart 해야 한다.[^1]

```
[2023-06-07 05:27:08,554: INFO/MainProcess] Task reviews.tasks.add[85a413d9-3ac5-478b-ba3d-f5930899fcf1] received
[2023-06-07 05:27:08,556: INFO/ForkPoolWorker-8] Task reviews.tasks.add[85a413d9-3ac5-478b-ba3d-f5930899fcf1] succeeded in 0.0005897910000385309s: 7
```

```python
from datetime import datetime, timedelta


add.apply_async((3,6), countdown=5)   # 또는 eta=datetime.now() + timedelta(minutes=1)
<AsyncResult: 94a4ff5b-ddff-4702-88e6-3d5da60f7528>
```

```
[2023-06-07 05:29:01,350: INFO/MainProcess] Task reviews.tasks.add[94a4ff5b-ddff-4702-88e6-3d5da60f7528] received
```
5초 후
```
[2023-06-07 05:29:06,349: INFO/ForkPoolWorker-8] Task reviews.tasks.add[94a4ff5b-ddff-4702-88e6-3d5da60f7528] succeeded in 0.00021904100049141562s: 9
```

<br>
settings/base.py
```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'remove-unused-tags-every-day': {
        'task': 'reviews.tasks.remove_unused_tags',
        'schedule': crontab(hour=5, minute=0),
    },
    'check-if-beat-is-up-and-running': {
        'task': 'reviews.tasks.check_beat',
        'schedule': 20,   # 20초마다 함수 실행
    },
}
```

# With Timezone

settings/base.py
```python
CELERY_TIMEZONE = 'Asia/Seoul'
```

<br>

# Daemonization


# 배포 환경에서

/etc/supervisor/conf.d
```
[program:myproject_celery_worker]
command=/path/to/your/virtualenv/bin/celery -A your_project_name worker --loglevel=info
directory=/path/to/your/project/
user=yourusername
numprocs=1
stdout_logfile=/path/to/your/logs/celery_worker.log
stderr_logfile=/path/to/your/logs/celery_worker.log
autostart=true
autorestart=true
startsecs=10

; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

[program:myproject_celery_beat]
command=/path/to/your/virtualenv/bin/celery -A your_project_name beat --loglevel=info
directory=/path/to/your/project/
user=yourusername
numprocs=1
stdout_logfile=/path/to/your/logs/celery_beat.log
stderr_logfile=/path/to/your/logs/celery_beat.log
autostart=true
autorestart=true
startsecs=10

[program:rabbitmq]
command=/usr/sbin/rabbitmq-server
user=rabbitmq
autostart=true
autorestart=true

```

---
# 참고자료
- [Check if celery beat is up and running](https://stackoverflow.com/questions/35355786/check-if-celery-beat-is-up-and-running)
- [Learn Django Celery with RabbitMQ - Install and create new celery instance, Run a simple task Part 1](https://youtu.be/fBfzE0yk97k)
- [How to Schedule Tasks in the Future With Celery](https://youtu.be/BR8RXQRpl7U)






[^1]: https://stackoverflow.com/questions/9769496/celery-received-unregistered-task-of-type-run-example
