---
created : 2023-04-03, Mon
topics : ModelForm과 그냥 Form의 차이
context : django, python
---
# [`ModelForm`과 그냥 `Form`의 차이](https://docs.djangoproject.com/en/3.2/topics/forms/#more-about-django-form-classes)
> In fact if your form is going to be used to directly add or edit a Django model, a ModelForm can save you a great deal of time, effort, and code, because it will build a form, along with the appropriate fields and their attributes, from a Model class.  

즉, 폼에서 입력된 값이 바로 모델에 적용되는 등 폼이 모델과 밀접하게 연결되어 있다면 `ModelForm`을 사용하라고 권한다.

**입력값이 데이터베이스에 저장 -> `ModelForm`, 다른 용도로 쓰인다면 -> `Form`**