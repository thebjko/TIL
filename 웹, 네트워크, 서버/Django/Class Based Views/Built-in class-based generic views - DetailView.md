---
created_at : 2023-04-28, Fri
유효기록일 : 2023-04-29, Sat
topics : 
context : Todo_ModelForm
tags : python/django/ClassBasedViews
related : 
---
# Built-in class-based generic views - DetailView
단순히 템플릿을 렌더링 할게 아니라면(TemplateView), 좀 더 특정한 목적을 가진 제네릭 뷰들에 대해 알아보자.

먼저, 4월 3일 실습 과제였던 ModelForm을 사용해 Todo 웹페이지를 만드는 프로젝트에 재방문했다. 다행히 데이터가 남아있어서 다시 만드는 번거로움을 덜었다.

todos/views.py
```python
 def detail(request, pk: int):
     context = {
         'data': Todo.objects.get(pk=pk),
     }
     return render(request, 'todos/detail.html', context)
```
기존 detail 뷰함수를 CBV로 리팩터하기 위해 임포트문을 작성하고 공식 문서를 따라 작성한다.
```python
from django.views.generic import DetailView

class TodoDetailView(DetailView):
    model = Todo
```
템플릿을 찾을 수 없다는 에러가 발생했다. 조상 클래스를 거슬러 올라가다보니 다음과 같은 클래스를 발견했다:
```python
class TemplateResponseMixin:
    """A mixin that can be used to render a template."""
    template_name = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None
```
얼른 `template_name`에 템플릿 이름을 할당했다.

> `template_name`이 전달되지 않으면 `todos/todo_detail.html`이 사용된다. `<프로젝트_이름>/<모델이름>_<디테일뷰니까_detail>.html`로 만들어지는 것 같다. (TemplateDoesNotExist 예외메세지) 

```python
class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todos/detail.html'
```
NoReverseMatch가 발생했다. `todos/detail.html` 파일은 원래 context에서 'data'를 받아 활용한다. 게시글 수정/삭제하는 버튼의 url이 `data.pk`를 필요로 했고, 적절히 전달되지 않아 예외가 발생했다.

공식 문서에서 다음과 같은 예를 찾았다:
```python
from django.views.generic import DetailView
from books.models import Publisher


class PublisherDetailView(DetailView):
    context_object_name = "publisher"
    queryset = Publisher.objects.all()   # model 변수 대신 사용
```
> queryset이 제공되지 않으면 model이 있는지 확인해 `all()`을 사용하고 둘 다 없으면 ImproperlyConfigured 예외를 발생시킨다.(`SingleObjectMixin` 소스코드 참조)

queryset에 전달된 데이터를 model 대신 사용해 부분만 사용할 수 있는 기능을 설명하는 부분이었는데, `context_object_name`이 눈에 띄었다. 얼른 사용해봤다.
```python
class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todos/detail.html'
    context_object_name = 'data'
```
성공적으로 작동했다. 
> `context_obejct_name`이 전달되지 않으면 모델 명을 lowercase 한 값으로 사용한다. (`SingleObjectMixin`의 `get_context_object_name` 소스코드)

todos/urls.py
```python
urlpatterns = [
    # path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/', views.TodoDetailView.as_view(), name='detail'),
]
```

<br>

## context로 다른 변수 넘겨주기
```python
class PublisherDetailView(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["book_list"] = Book.objects.all()
        return context
```
실험삼아 다음과 같이 임의의 키에 임의의 값을 전달했다:
```python
	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # {{ abc }} 로 사용
        context['abc'] = 'efg'   # d is silent
        return context
```
성공적으로 템플릿에 전달되었다.
![[get_context_data.png]]

<br>

## Dynamic Filtering

urls.py가 다음과 같다고 하자
```python
# urls.py
from django.urls import path
from books.views import PublisherBookListView

urlpatterns = [
    path("books/<publisher>/", PublisherBookListView.as_view()),
]
```
위의 예에서는 pk를 어디에도 전달하지 않았음에도 detail 뷰가 자연스럽게 활용했다. 그렇다면 publisher도 그럴까? URL로 전달된 값을 CBV는 어떻게 활용할까? 

```python
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from books.models import Book, Publisher


class PublisherBookListView(ListView):
    template_name = "books/books_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
        return Book.objects.filter(publisher=self.publisher)
```
위의 예는 `self.kwargs["publisher"]`로 URL에 전달된 publisher 값을 받아 Book 데이터를 필터링하는데 사용하고 있다. pk는 전달하지 않아도 'pk'를 기본키를 kwargs에서 가져오기 위해 사용한다(`pk_url_kwarg`의 default).  `pk_url_kwarg = 'abc'`처럼 이상한 값을 지정하면 에러가 발생한다.

<br>

## Performing extra work
Author 모델 레코드를 누군가가 열람할 때마다 `last_accessed` 필드 값을 업데이트하고싶다고 하자.
```python
# models.py
from django.db import models


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to="author_headshots")
    last_accessed = models.DateTimeField()
```

```python
# urls.py
from django.urls import path
from books.views import AuthorDetailView

urlpatterns = [
    # ...
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
]
```

```python
from django.utils import timezone
from django.views.generic import DetailView
from books.models import Author


class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj
```

`get_object`메서드를 오버라이드 함으로 구현할 수 있다. 

DetailView의 부모클래스인 BaseDetailView의 get 메서드에서 `get_object()`가 실행된다. queryset을 인자로 넘겨받으며, 전달된 값이 없으면 model을 찾는다

> 📝 Mixin 관련  
> DetailView는 SingleObjectMixin과 BaseDetailView를 상속한다. BaseDetailView에서 사용되는 self 키워드는 SingleObjectMixin을 가리키기 위해 사용할 수 도 있는 것 같다. 파이썬에서 다중 상속은 구분된 클래스를 따로 상속한다기 보다는 두개를 섞어 만든 하나의 클래스를 상속하는 것이라고 이해할 수 있을 듯 하다.

📝 [메서드와 기능들에 대한 다른 설명은 API Reference를 참고하자.](https://docs.djangoproject.com/en/4.2/ref/class-based-views/)

<br>

---
# 참고자료
- https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/

