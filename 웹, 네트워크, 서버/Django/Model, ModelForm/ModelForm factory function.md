---
created : 2023-04-03, Mon
topics : ModelForm factory function
context : django, python
tags : python/django/ModelForm
---
# [ModelForm factory function](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#modelform-factory-function)
> 클래스 정의 대신 사용할 수 있는 팩토리 메서드

예시
```python
>>> from django.forms import modelform_factory
>>> from myapp.models import Book
>>> BookForm = modelform_factory(Book, fields=("author", "title"))

>>> from django.forms import Textarea
>>> Form = modelform_factory(Book, form=BookForm, widgets={"title": Textarea()})
```