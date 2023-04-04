---
created : 2023-04-03, Mon
topics : BoundField
context : django
tags: python/django/Forms_API
---
# [BoundField](https://docs.djangoproject.com/en/3.2/ref/forms/api/#django.forms.BoundField)
> Used to **display HTML** or **access attributes** for a single field of a Form instance.

아래와 같이 사용한다.
```python
>>> form = ContactForm()
>>> for boundfield in form: print(boundfield)
<input id="id_subject" type="text" name="subject" maxlength="100" required>
<input type="text" name="message" id="id_message" required>
<input type="email" name="sender" id="id_sender" required>
<input type="checkbox" name="cc_myself" id="id_cc_myself">
```

필요에 따라 아래의 자료를 살펴보라
- [Attributes of BoundField](https://docs.djangoproject.com/en/3.2/ref/forms/api/#attributes-of-boundfield)
- [Methods of BoundField](https://docs.djangoproject.com/en/3.2/ref/forms/api/#methods-of-boundfield)
- [Customizing BoundField](https://docs.djangoproject.com/en/3.2/ref/forms/api/#customizing-boundfield)

---
# 참고자료
- Django 공식문서 (v3.2)