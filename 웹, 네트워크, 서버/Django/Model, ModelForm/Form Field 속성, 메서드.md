---
created : 2023-04-03, Mon
topics : Form Field 속성, 메서드
context : Todo_ModelForm 프로젝트, 템플릿
tags : python/django/FormField/methods python/django/template_language
---
# [Form Field 속성, 메서드](https://docs.djangoproject.com/en/3.2/topics/forms/#looping-over-the-form-s-fields)
> [[Widgets 사용법, 예시, 필드 클래스#^0dce50]]를 보라  
> [[BoundField]] 참조

## 예시
```python
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}
```

## `{{ field.label }}`
- label 값을 보여줌

## `{{ field.label_tag }}`
- html의 label 태그 전체를 보여줌  
- ex. `<label for="id_email">Email address:</label>`

## `{{ field.id_for_label }}`
- label 태그의 id를 보여줌

## `{{ field.value }}`
- value 속성의 값을 보여줌

## `{{ field.html_name }}`
- input 요소의 name 속성에 사용할 수 있는 name 값을 보여줌

## `{{ field.help_text }}`
- 연관된 help text를 보여줌
- ex. ?

## `{{ field.errors }}`
- 유효성 검사에서 실패한다면, `<ul class="errorlist">` 안에 들어가는 값을 보여줌

## `{{ field.is_hidden }}`
- 폼 필드가 `hidden`이라면 `True`, 아니라면 `False`를 리턴

## `{{ field.field }}`
- The Field instance from the form class that this [[BoundField|`BoundField`]] wraps. **You can use it to access Field attributes**, e.g. `{{ char_field.field.max_length }}`.

---
# 참고자료
- Django 공식문서 (v3.2)