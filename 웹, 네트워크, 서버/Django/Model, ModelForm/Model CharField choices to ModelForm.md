---
created_at : 2023-04-06, Thu
유효기록일 : 2023-04-06, Thu
topics : Django Model, ModelForm
context : Model Field Reference
tags : python/django/forms/modelform python/django/model
related : Model Field Reference
---
# Model CharField choices -> ModelForm
[[각 모델 필드와 해당하는 디폴트 필드 타입|Django Model에는 필드에 사용할 수 있는 ChoiceField 타입이 없다.]] 대신 CharField 타입의 choices 속성을 사용해 해당 모델로 ModelForm을 만들었을 때 select 요소로 입력할 수 있게 된다.

아래는 공식 문서의 예시이다.

```python
from django.db import models

class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {self.JUNIOR, self.SENIOR}
```

<br><br>

🛠 **DevShare 프로젝트 예시(test)** 🛠

models.py
```python
class Category(models.Model):
    DEV = '개발'
    NEW_TECH = '신기술'
    CS = 'CS'
    CHOICES = [
        (DEV, '개발'),
        (NEW_TECH, '신기술'),
        (CS, 'CS'),
    ]
    category = models.CharField(
        max_length=10,   # 필수 입력값
        choices=CHOICES,
    )
```

forms.py
```python
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
```

category.html
```django
{% extends 'base.html' %}

{% block content %}
{{ form.as_p }}
{% endblock content %}
```

views.py
```python
def test_category(request):
    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/category.html', context)
```

⭐️ 출력된 태그
```html
<p>
  <label for="id_category">Category:</label>
  <select name="category" required="" id="id_category">
    <option value="" selected="">---------</option>
    <option value="개발">개발</option>
    <option value="신기술">신기술</option>
    <option value="CS">CS</option>
  </select>
</p>
```

---
# 관련자료
- [Model Field Reference : Choices](https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-choices)

[^1]: