---
created_at : 2023-04-29, Sat
유효기록일 : 2023-04-29, Sat
topics : 
context : Todo_ModelForm
tags : python/django/CBV
related : 
---
# CreateView
기존 create 뷰함수:
```python
def create(request):
    # HTTP request가 POST라면 게시글 작성 로직 진행
    if request.method == 'POST':
        form = TodoForm(data=request.POST)
        if form.is_valid():
            todo = form.save()
            return redirect('todos:detail', todo.pk)
    # 아니라면 작성 페이지 응답
    else:
        form = TodoForm()
    return render(request, 'todos/create.html', {'form': form})
```

CreateView 클래스를 사용해 CBV로 리팩터해보자.

1. `model`과 `template_name` 작성
```python
class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todos/create.html'
```
이대로라면 에러가 발생한다. 작성할 Fields가 제공되지 않았다는 ImproperlyConfigured 에러인데, Form을 그냥 만들어주지는 않나보다. fields 속성에 값을 할당하고 `get_form` 메서드에서 위젯을 지정하는 어려운 방법이 있는데, 여기서는 그냥 `form_class`에 forms.py의 TodoForm을 할당해주기로 한다(1).

2. Todo 모델에 `get_absolute_url` 정의
여기서 url을 제공하거나 `get_absolute_url` 메서드를 정의하라는 에러가 발생한다. 생성 후 생성된 detail 페이지로 이동할 것이므로 인스턴스의 정보가 필요해 `success_url` 속성을 정의하는 대신, **Todo 모델에** `get_absolute_url` 속성을 정의하자(2).
```python
class Todo(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField(null=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=3)
    created_at = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True)
    
    def get_absolute_url(self):
        return reverse_lazy('todos:detail', kwargs={'pk': self.pk})
```

3. create.html
```django
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit" class="btn btn-primary">
    만들기
  </button>
</form>
```
form 요소에서 action 속성을 뺐다.

<br>

# UpdateView

기존 update 뷰함수:
```python
def update(request, pk: int):
    todo = Todo.objects.get(pk=pk)
    # HTTP request method가 POST라면
    if request.method == 'POST':
        form = TodoForm(data=request.POST, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect('todos:detail', todo.pk)
    # 아니라면
    else:
        form = TodoForm(instance=todo)
    context = {
        'form': form,
        'todo': todo,
    }
    return render(request, 'todos/update.html', context)
```

CreateView처럼 아래와 같이 쉽게 작성할 수 있다.
```python
class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todos/update.html'
    form_class = TodoForm
```

detail.html
```django
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit" class="btn btn-primary">수정내용 저장</button>
</form>
```

<br>

---
# 참고자료
1. https://stackoverflow.com/questions/27321692/override-a-django-generic-class-based-view-widget
2. https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-editing/#model-forms

[^1]: