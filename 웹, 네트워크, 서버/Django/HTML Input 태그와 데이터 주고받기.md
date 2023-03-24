---
created : 2023-03-23, Thu
topics : throw and catch, interaction with input element, name attribute
context : 
---
# HTML Input 태그와 데이터 주고받기
> HTML의 input 요소와 상호작용하는 법

## 3월 23일 실습, 어플리케이션 "throw_and_catch"
```html
{% extends 'base.html' %}

{% block title %}
Throw
{% endblock title %}

{% block content %}
<form action="{% url 'throw_and_catch:catch' %}">
  <label for="message">Message : </label>
  <input type="text" name="message" placeholder="내용을 입력하세요">
  <button type="submit" class="btn btn-info">Info</button>
</form>
{% endblock content %}
```

urls.py
```python
from django.shortcuts import render

def throw(request):
    return render(request, 'throw_and_catch/throw.html')


def catch(request):
    context = {
        "data": request.GET["message"],   # input 요소의 name 속성에 할당된 값을 호출해 입력값을 불러온다.
    }
    return render(request, 'throw_and_catch/catch.html', context)
```
> input 요소의 name 속성에 할당된 값을 호출해 입력값을 불러온다.

catch.html
```python
{% extends 'base.html' %}

{% block title %}
Catch
{% endblock title %}

{% block content %}
<h1>{{ data }}</h1>   {# input 태그에 입력된 값을 context로 전달받아 data로 사용 #}
<a href="{% url 'throw_and_catch:throw' %}">
  <button type="button" class="btn btn-link">뒤로가기</button>
</a>
{% endblock content %}
```
input 태그에 입력된 값을 context로 전달받아 키 값인 "data"로 [[Filter, Tag, Variable#^1b325c|variable]] 사용


## 3월 22일 실습, 어플리케이션 "lotto"
lotto_create.html
```html
{% extends 'base.html' %}

{% block title %}
로또 번호 생성기
{% endblock title %}

{% block content %}
<div class="input-group mb-3">
  <form action="/lotto/" class="d-flex">
    <input type="number" name="how-many" class="form-control my-3 me-1" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" placeholder="몇 개를 생성할까요?">
    <button class="btn btn-outline-secondary text-nowrap my-3" type="submit" id="button-addon2" disabled>생성</button>
  </form>
</div>
{% endblock content %}

{% block script %}
<script>
  const inputTag = document.querySelector('input')
  const btn = document.querySelector('button')
  inputTag.addEventListener('input', (e) => {
    if (e.target.value.trim()) {
      btn.disabled = false
    } else {
      btn.disabled = true
    }
  })
</script>
{% endblock script %}
```
> `name` 속성이 아니라 `id`로도 된다. 

views.py
```python
from django.shortcuts import render
from random import *

def lotto_create(request):
    return render(request, 'lotto/lotto_create.html')


numbers = list(range(1,46))
def lotto(request):
    context = {
        "numbers": [],
    }
    for _ in range(int(request.GET["how-many"])):
        context["numbers"].append(sorted(sample(numbers, 6)))
    
    return render(request, 'lotto/lotto.html', context)

```

lotto.html
```html
{% extends 'base.html' %}

{% block title %}
당신의 행운의 번호는 ...
{% endblock title %}

{% block content %}

{% for n in numbers %}
  <h1>{{ n|join:", " }}</h1>
{% endfor %}
<a href="/lotto-create/">
  <button type="button" class="btn btn-link">뒤로가기</button>
</a>
{% endblock content %}
```

---
`name` 속성이 `label`요소와 `input` 요소를 묶어주고, django로 데이터를 전달하는 키 역할을 한다.