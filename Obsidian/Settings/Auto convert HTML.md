---
created : 2023-03-24, Fri
topics : obsidian settings, Auto convert HTML,
context : 옵시디언, settings, VSCode,
---
# Auto convert HTML 활성화에 따른 VSCode로부터 코드 복사 및 붙여넣기
version :: 1.1.16
## 켜져 있을 때 :
```python
from django.db import models

  

class Article(models.Model):

# 하나의 모델 클래스는 하나의 테이블 스키마를 작성하는 것이다.

# Field Name(Class Variable Name), Data Type(Model Field Class), Constraints

# 아이디는 django가 자동 생성

# Field Name = Data Type(Constraints)

title = models.CharField(max_length=50)

content = models.TextField()

created_at = models.DateTimeField(auto_now_add=True)

updated_at = models.DateTimeField(auto_now=True)
```
## 꺼져있을 때 :
```python
from django.db import models

class Article(models.Model):
    # 하나의 모델 클래스는 하나의 테이블 스키마를 작성하는 것이다.
    # Field Name(Class Variable Name), Data Type(Model Field Class), Constraints
    # 아이디는 django가 자동 생성
    # Field Name = Data Type(Constraints)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


```

📝 Auto convert HTML은 Editor 섹션에 있다.