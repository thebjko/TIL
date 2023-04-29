---
created_at : 2023-04-29, Sat
유효기록일 : 2023-04-29, Sat
topics : 
context : Todo_ModelForm
tags : python/django/CBV
related : 
---
# DeleteView
```python
def delete(_, pk):
    Todo.objects.get(pk=pk).delete()
    return redirect('todos:index')
```
위 기존 코드를 아래와 같이 리팩터했다.

```python
class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy('todos:index')
    template_name = 'todos/confirm.html'   # confirm deletion page

todo_delete_view = TodoDeleteView.as_view()
```
GET 메서드를 사용해 요청하면 `template_name`에 할당된 템플릿으로 이동한다. 주로 삭제를 확인하기 위해 사용하며, 확인 템플릿에서는 POST메서드로 다시 요청한다.
```python
<form method="post">{% csrf_token %}
    <p>Are you sure you want to delete "{{ object }}"?</p>
    {{ form }}
    <input type="submit" value="Confirm">
</form>
```
form 요소의 action 속성을 사용하지 않는다. 

- `success_url` : 삭제 성공시 이동할 URL을 할당한다. 하드코딩(`/todos/index/`)도 가능하고 `reverse` 함수를 사용할수도 있다. [[reverse(), resolve()]] 참고.

만약 확인 페이지를 사용하지 않고 바로 삭제하고 싶다면 POST메서드로 삭제하면 된다.
```django
<a href="{% url 'todos:delete' data.pk %}" class="card-link">삭제</a>
```
위 코드를 아래와 같이 변경.
```django
<form action="{% url 'todos:delete' data.pk %}" method="post">
  {% csrf_token %}
  <button type="submit">삭제</button>
</form>
```

그런데 뒤로가기시 다시 확인할 수 있다는 문제가 생긴다. 

<br>

# RedirectView

```python
# project/views.py
from django.urls import reverse_lazy
from django.views.generic import RedirectView

# def index(request):
#     return redirect('todos/')

class TodoRedirectView(RedirectView):
    url = reverse_lazy('todos:index')

todo_redirect_view = TodoRedirectView.as_view()
```

<br>

---
# 참고자료
- https://stackoverflow.com/questions/17475324/django-deleteview-without-confirmation-template
- https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#deleteview