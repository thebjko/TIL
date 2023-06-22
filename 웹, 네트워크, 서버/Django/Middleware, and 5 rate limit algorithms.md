---
created_at : 2023-06-21, Wed
유효기록일 : 2023-06-22, Thu
topics : 
context : 
tags : django middleware api_gateway rate_limit
related : 
---
> 미들웨어에 대해 공부하고, 이에 대한 이해를 바탕으로 정리한 글입니다.

# 미들웨어란?
웹에서 Django 어플리케이션으로 요청(request)이 들어오면 Django 어플리케이션은 그에 대한 응답(response)을 반환한다. 요청과 응답이 들어오고 나갈 때, 이 값을 전역에서 변환하고자 할 때 사용한다. 일례로 API Gateway가 있다.

사용자 요청이 들어올 때, WSGI 핸들러 인스턴스가 생성된다. WSGI 핸들러는 아래의 작업들을 수행한다:

1. `settings.py` 파일과 Django 예외 클래스들을 임포트한다.
2. `settings.py` 파일에 기록된 미들웨어 클래스들을 불러온다.
3. 요청, 뷰, 응답, 예외를 처리하는 메서드 리스트를 만든다.
4. 요청 메서드를 순차적으로 순회한다.
5. 요청된 URL을 resolve 한다.
6. 뷰를 처리하는 메서드를 순회한다.
7. 뷰 함수를 호출한다.
8. 예외 메서드를 처리한다.
9. 응답 메서드를 요청 메서드의 반대 순서로 순회한다.
10. 리턴 값을 만들고 콜백 함수를 호출한다.

아직 위의 모든 것들이 미들웨어에서 이루어지는지는 모르겠다. 하지만 4번과 9번이 시사하는 바, 요청은 `MIDDLEWARE` 리스트에 있는 순서대로 처리가 되고, 응답은 그 반대로 처리된다.

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## 커스텀 미들웨어 만들기
- 파이썬 패키지 만들기 : `__init__.py`가 들어있는 폴더를 만들고 그 안에 파이썬 파일을 만든다. 아니면 그냥 어플리케이션 안에 바로 미들웨어 파일을 만들 수도 있다.
- 함수로 만들수도 있고, 클래스로 만들수도 있다.

함수 기반 미들웨어:
```python
def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
    
	    # 뷰가 호출되기 전에 각 request에 대해 실행할 코드

        response = get_response(request)

        # 뷰가 호출된 후 각 request/response에 대해 실행할 코드

        return response

    return middleware
```
`get_response` 함수를 전달받아 실행된다. `request`에 대한 작업을 실행하고, `request`에 대한 응답(`response`)을 `get_response`를 통해 받는다. 이후 `response`에 대한 작업을 수행한 뒤 반환한다.

`get_response` 콜러블 객체는 뷰일수도 있고(좀 더 정확히 말하면 각 URL에 해당하는 뷰를 적절하게 불러오는 미들웨어와, 템플릿 응답과 예외를 담당하는 미들웨어를 적용하는 wrapper), 다음 미들웨어일 수도 있다. 

클래스 기반 미들웨어:
```Python
class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # 뷰가 호출되기 전 각 request에 대해 실행할 코드

        response = self.get_response(request)

        # 뷰가 호출된 후 각 request/response에 대해 실행할 코드
        return response

    def process_view(request, view_func, view_args, view_kwargs) -> None | HttpResponse:
        # Django가 뷰를 호출하기 직전 실행된다
        # None 또는 HttpResponse 객체를 반환해야 한다.
        # 뷰가 호출되기 전에 request.POST에 접근한다면 이후에 실행될 미들웨어에서 업로드 핸들러를 조작할 수 없게 된다. CsrfViewMiddleware는 예외.
        return None

    def process_exception(request, exception) -> None | HttpResponse:
        # 뷰가 예외를 발생시키면 Django는 이 메서드를 호출한다.
        # None 또는 HttpResponse 객체를 반환해야 한다.
        # HttpResponse → 템플릿 응답과 Response Middleware가 적용되어 해당 응답이 반환됨.
        # None → 기본 예외 처리
        return None

    def process_template_response(request, response):
        # View가 실행된 후, 응답이 render() 메서드를 포함할 경우 실행된다. 
        # 이 경우 응답이 TemplateResponse 또는 그와 동등해야 한다고 한다. 
        # render() 메서드를 사용하는 응답 객체를 반환해야 한다. 
        # 예를 들어 TemplateResponse를 상속하는 클래스를 반환할 수 있다.
        return response
```
인스턴스가 생성될 때 `get_response` 함수를 전달받는다. 이 미들웨어의 인스턴스가 호출되면 `response`가 반환된다. 

<br>

# 더 공부해 볼 주제
- rate limit 알고리즘 구현하기
- `StreamingHttpResponse` 다루기

<br>

---
# 참고자료
- [Everything you need to know about Middleware in Django!](https://medium.com/scalereal/everything-you-need-to-know-about-middleware-in-django-2a3bd3853cd6)
- [Django Doc 4.2 on Middleware](https://docs.djangoproject.com/en/4.2/topics/http/middleware/)

[^1]: 
