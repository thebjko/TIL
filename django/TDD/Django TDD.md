---
created_at : <% tp.file.creation_date("YYYY-MM-DD, ddd") %>
유효기록일 : <% tp.date.now("YYYY-MM-DD, ddd") %>
topics : 
context : 
tags : django TDD test-driven-development
related : 
---
# Django TDD
Django TDD란 Django 프레임워크를 사용하여 개발할 때, Test Driven Development(TDD) 방식으로 개발하는 것을 말합니다.

TDD는 소프트웨어를 개발할 때, 먼저 테스트 코드를 작성하고 이를 통과할 만큼의 최소한의 코드를 작성한 후에 리팩토링을 하는 개발 방법론입니다. 이 방법을 통해 코드 품질을 높이고 유지 보수성을 높일 수 있습니다.

Django TDD를 적용하려면, Django의 내장된 테스트 프레임워크를 사용하면 됩니다. Django의 테스트 프레임워크는 `TestCase` 클래스를 상속받아 테스트를 작성할 수 있도록 지원합니다.

예를 들어, Django TDD를 이용하여 간단한 블로그 애플리케이션을 개발한다고 가정해봅시다.

먼저, 테스트를 작성합니다.

```python
from django.test import TestCase
from django.urls import reverse
from blog.models import Post

class PostModelTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Test post', body='This is a test')

    def test_title_content(self):
        post = Post.objects.get(id=1)
        expected_object_title = f'{post.title}'
        self.assertEquals(expected_object_title, 'Test post')

    def test_body_content(self):
        post= Post.objects.get(id=1)
        expected_object_body = f'{post.body}'
        self.assertEquals(expected_object_body, 'This is a test')

class HomePageViewTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Test post', body='This is a test')

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')

```

그리고 나서, 테스트를 실행하고 이를 통과할 만큼의 코드를 작성합니다.

```python
from django.shortcuts import render
from blog.models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

```

위의 코드에서, home view 함수는 `Post` 모델에서 모든 게시물을 가져와 이를 home.html 템플릿에 전달하는 역할을 합니다.

마지막으로, 리팩토링을 하면서 코드 품질을 높입니다.

<br>

# 4.2
먼저, blog 앱의 models.py 파일에 `Post` 모델을 작성합니다.
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

```

다음으로, blog 앱의 tests.py 파일에 `Post` 모델에 대한 테스트를 작성합니다.

```python
from django.test import TestCase
from blog.models import Post

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Test post', body='This is a test')

    def test_title_content(self):
        post = Post.objects.get(id=1)
        expected_object_title = f'{post.title}'
        self.assertEqual(expected_object_title, 'Test post')

    def test_body_content(self):
        post = Post.objects.get(id=1)
        expected_object_body = f'{post.body}'
        self.assertEqual(expected_object_body, 'This is a test')

```
그 다음으로, blog 앱의 views.py 파일에 home view 함수를 작성합니다.
```python
from django.shortcuts import render
from blog.models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

```
마지막으로, blog 앱의 tests.py 파일에 home view 함수에 대한 테스트를 작성합니다.
```python
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post

class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Test post', body='This is a test')

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')

    def test_view_returns_posts(self):
        resp = self.client.get(reverse('home'))
        posts = resp.context['posts']
        self.assertTrue(len(posts) > 0)

```

위와 같은 방식으로 Django 4.2 버전에서 TDD를 적용한 코드를 작성할 수 있습니다. 코드 작성 후 `python manage.py test` 명령어를 통해 작성한 테스트를 실행할 수 있습니다.

`client`는 Django의 기본 테스트 프레임워크를 사용하여 테스트 케이스를 작성할 때 자동으로 생성되는 Client의 인스턴스이다. 이 클래스의 인스턴스를 직접 생성할 필요는 없으며, Django의 `TestCase` 클래스를 상속받는 테스트 케이스 클래스에서 self.client 속성을 통해 접근할 수 있다.

<br>

# assert 함수의 종류
- `assertEqual(a, b)` : a와 b가 같은지 확인합니다.
- `assertNotEqual(a, b)` : a와 b가 다른지 확인합니다.
- `assertTrue(x)` : x가 참인지 확인합니다.
- `assertFalse(x)` : x가 거짓인지 확인합니다.
- `assertIs(a, b)` : a와 b가 동일한 객체인지 확인합니다.
- `assertIsNot(a, b)` : a와 b가 동일한 객체가 아닌지 확인합니다.
- `assertIsNone(x)` : x가 None인지 확인합니다.
- `assertIsNotNone(x)` : x가 None이 아닌지 확인합니다.
- `assertIn(a, b)` : a가 b 안에 포함되어 있는지 확인합니다.
- `assertNotIn(a, b)` : a가 b 안에 포함되어 있지 않은지 확인합니다.
- `assertIsInstance(a, b)` : a가 b의 인스턴스인지 확인합니다.
- `assertNotIsInstance(a, b)` : a가 b의 인스턴스가 아닌지 확인합니다.

`TestCase`의 메서드이므로 클래스 내에서 확인할 수도 있다.

<br>

# Template 테스트하기
blog 앱의 home.html 템플릿이 제대로 작동하는지 확인하기 위해, 다음과 같이 테스트를 작성
```python
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post

class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Test post', body='This is a test')

    def test_homepage_contains_correct_html(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<title>Blog home</title>')
        self.assertContains(resp, '<h1>Blog home</h1>')

    def test_homepage_does_not_contain_incorrect_html(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'Hi there! I should not be on the page.')

```
위의 테스트는 home 뷰 함수가 home.html 템플릿을 올바르게 렌더링하고 있는지를 확인합니다. `test_homepage_contains_correct_html` 메서드는 home.html 템플릿이 <title> 태그와 <h1> 태그를 포함하는지를 확인하고, `test_homepage_does_not_contain_incorrect_html` 메서드는 템플릿이 잘못된 HTML을 포함하지 않는지를 확인합니다.

`assertContains`와 `assertNotContains` 메서드는 `HttpResponse` 객체에 대해, 해당 문자열이 포함되어 있는지 여부를 검사합니다. 이를 통해 템플릿이 예상한 대로 HTML을 생성하고 있음을 확인할 수 있습니다.

템플릿 테스트는 템플릿 디자인이나 HTML 구조를 변경할 때 유용하게 활용될 수 있습니다.

<br>

---
# 참고자료
1. https://docs.djangoproject.com/en/3.2/topics/testing/
2. ChatGPT
