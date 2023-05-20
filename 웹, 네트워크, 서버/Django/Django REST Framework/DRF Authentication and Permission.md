---
created_at : 2023-05-18, Thu
유효기록일 : 2023-05-20, Sat
topics : 
context : 
tags : drf django_REST_Framework
related : 
---
# DRF Authentication and Permission
DRF는 로그인 창도 없는데 사용자 인증을 어떻게 처리할까? 

<br>

## 1. 로그인 한 사용자에게만 기능 허락하기
```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
		...
```
현재 위와 같이 `ListCreateAPIView`가 구현되어있다. 이 뷰 클래스에 특정한 권한을 가진 유저만 접근할 수 있도록 authentication과 permission을 추가할 것이다. 

```python
from rest_framework import generics, permissions, authentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
		...

```

`permissions`와 `authentication`을 `rest_framework`에서 임포트하고 위와 같이 설정한다.

<br>

### Authentication의 몇 가지 예
- `SessionAuthentication` : Returns a `User` if the request session currently has a logged in user. Otherwise returns `None`.
- `TokenAuthentication` : headers로 토큰을 넘겨 인증받는 방식
- `RemoteUserAuthentication` : 환경변수에 `REMOTE_USER`를 선언하고 사용한다.

<br>

## 2.`DjangoModelPermissions`으로 특정 메서드에 대한 권한 허용하기
```python
from rest_framework import generics, permissions, authentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
		...

```
`permission_classes`를 `DjangoModelPermissions`으로 변경하면, Admin 사이트에서 부여한 권한만 갖도록 설정할 수 있다. `permission_classes`가 설정된 뷰에 대해서, `POST`, `PUT`, `PATCH`, `DELETE` 메서드에 대해서만 적용된다.

`DjangoModelPermissions`는 `django.contrib.auth`의 model permissions와 연결되어 있다고 한다. 이 permissions는 Model `Meta` 클래스의 `permissions` 속성을 정의함으로 해당 모델에 대한 권한 종류를 정의한다. 따라서 `DjangoModelPermissions`는 `.queryset` 속성이나 `get_queryset()` 메서드를 가진 뷰에서 사용해야 한다.[^3]

공식 문서의 예를 보자.
```python
class Task(models.Model):
    ...

    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]
```
`Task` 모델의 `Meta` 클래스는 `change_task_status`, `close_task`라는 `permissions`를 갖고 있다. 이 모델의 변경사항 migrate 후 `user.has_perm('app.close_task')`와 같은 형태로 어떤 유저가 해당 권한을 갖고 있는지 확인할 수 있다.[^2] `has_perm` 메서드의 인수는 `<app label>.<permission codename>`과 같은 형태로 전달한다. [^1]

<br>

## 3. `DjangoModelPermissions` 커스텀하기
아직 staff 유저에게 모든 권한을 제거해도 `ListCreateAPIView`에 GET 요청을 보내면 여전히 모든 product 정보를 확인할 수 있다.

`DjangoModelPermissions` 소스코드
```python
class DjangoModelPermissions(BasePermission):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    ...

```

`perms_map`은 `POST`, `PUT`, `PATCH`, `DELETE` 메서드에 대해서만 권한을 적용할 수 있도록 하고 있다. `GET` 메서드에 대해선 누구나 허용되고 있다.

products/permissions.py
```python
from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    '''
    이 클래스가 permission_classes에 추가된 뷰에 대해서 GET, POST, PUT, PATCH, DELETE 메서드의 권한을 지정할 수 있다.
    '''
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
	...
```

`GET` 메서드에 대해서도 권한을 설정하기 위해 permissions.py 파일을 만들고 `DjangoModelPermissions`를 오버라이드한다. `GET` 메서드 값에 위와 같이 입력한다. 각 권한은 `"<app label>.<permission codename>"`과 같은 형태로 되어있다. permission codename은 add, change, delete, 또는 view와 언더스코어 그리고 모델 이름으로 구성되어있다. 이름에서 알수 있듯, view는 조회, change는 변경, delete는 삭제를 의미한다. 예를 들어 api 앱의 product 모델에 대한 조회권한은 `'api.view_product'`가 된다. `DjangoModelPermissions` 클래스의 `get_required_permissions` 메서드에서 형태가 완성된다. (컨벤션 같은 느낌이다. `has_perm` 메서드를 실행할 때 기억하기 쉽게 하기 위함인 것 같다. 예를 들어 `'GET': ['%(app_label)s.change_%(model_name)s']`라고 해도 조회가 가능했다.)

```python
	def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

```
또 Django에서 user가 사용할 수 있는 인증 메서드를 제공하니 확인해보자. `has_perm`과 같은 메서드로 권한을 조회할 수 있다.[^1]

<br>

## 4. Token Authentication
DRF에서 기본적으로 제공하는 인증 방법중 하나. 

settings.py
```python
INSTALLED_APPS += ['rest_framework.authtoken']
```
migrate → 이후 admin site에서 'Token' 확인 가능

api/urls.py
```python
from rest_framework.authtoken.views import obtain_auth_token

...

urlpatterns += [path('auth/', obtain_auth_token)]
```
이후 해당 경로를 호출해 token을 얻을 수 있다.

products/views.py
```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]

```
client/list.py
```python
import requests
from getpass import getpass   # Portable password input
auth_endpoint = "http://localhost:8000/api/auth/"

auth_response = requests.post(auth_endpoint, json={
    'username': input('Username: '),
    'password': getpass(),
})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": "Token %s" %token,
    }
    endpoint = "http://localhost:8000/api/products/"

    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())

```
post메서드 json 인자에 username과 password를 전달한다. 토큰은 `auth_response.json()['token']`에서 확인할 수 있다. 이 값을 header에 위와 같이 전달해 endpoint를 조회할 수 있다. 

이 외에도 signal을 사용하거나 Django admin을 사용해 토큰을 생성할 수 있다. 토큰을 생성하는 다른 방법들은 공식 문서를 참고하자.[^4] 여기서 토큰을 생성하는 뷰를 커스텀하는 예도 볼 수 있다. 이를 통해 `user_id`나 `email` 같은 다른 정보도 토큰과 같이 전달할 수 있다.

<br>

### 토큰 전달 키워드를 변경하고 싶은 경우
아래의 예는 키워드를 Token에서 Bearer로 변경한다.

api/authentication.py
```python
from rest_framework.authentication import TokenAuthentication as BaseTokenAuth

class TokenAuthentication(BaseTokenAuth):
    keyword = 'Bearer'
```
products/views.py
```python
from api.authentication import TokenAuthentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication,
    ]

```
client/list.py
```python
if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": "Bearer %s" %token,
    }
    endpoint = "http://localhost:8000/api/products/"

    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())

```

<br>

### Token 삭제하기
admin site에서 직접 삭제하거나 만료시점을 지정할 수 있다.

생성된 Token 객체에는 생성일자가 기록되어 있다.

shell_plus
```python
In [1]: locals()
Out[1]: 
{
 ...
 'Token': rest_framework.authtoken.models.Token,
 ...
 }

In [2]: Token
Out[2]: rest_framework.authtoken.models.Token

In [3]: Token.objects.all().first()
Out[3]: <Token: 7a2f2f5dbe73de7b41caf0c125128a88faf3c3ff>

In [4]: dir(Token.objects.first())
Out[4]: 
[...
 'created',
 ...]

In [5]: token_obj = Token.objects.first()

In [6]: token_obj.created
Out[6]: datetime.datetime(2023, 5, 16, 11, 30, 39, 708960, tzinfo=<UTC>)

```
이를 사용해 CRON Job 또는 Celery로 토큰을 삭제하는 작업을 할 수 있다.

<br>

## 5. Default 권한 설정하기
매 뷰마다 `authentication_classes`, `permission_classes`를 작성하지 않기 위해 모든 뷰에 적용되는 권한을 설정해보자. 

settings.py
```python
auth_classes = (
    'rest_framework.authentication.SessionAuthentication',
    'api.authentication.TokenAuthentication',
)

if DEBUG:
    auth_classes = (
        'api.authentication.TokenAuthentication',
    )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': auth_classes,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}
```

위와 같이 작성하고, 오버라이드 해야 할 경우 뷰에서 작성한다.

<br>

## 6. Permission Mixin
Mixin 클래스를 사용해 permission을 관리하자.

> product/permissions.py → api/products.py 로 위치 변경 후 진행.

api/mixins.py
```python
from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin:
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
```
`permissions.IsAdminUser` 권한이 먼저 적용되고 `IsStaffEditorPermission`이 적용된다.

products/views.py
```python
...

from api.mixins import StaffEditorPermissionMixin


class ProductListCreateAPIView(
	    StaffEditorPermissionMixin,
	    generics.ListCreateAPIView,
	):
	...


class ProductDetailAPIView(
	    StaffEditorPermissionMixin,
	    generics.RetrieveAPIView,
	):
	...

...

```
기존 `permission_classes` 속성은 삭제한다.

<br>

---
# 참고자료
- [Build a Django REST API with the Django Rest Framework. Complete Tutorial. - CodingEntrepreneurs](https://youtu.be/c708Nf0cHrs)


[^1]: [`has_perm` Method on User (Django Doc 4.2)](https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.User.has_perm)
[^2]: [Django Custom Permission (Django Doc 4.2)](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#custom-permissions)
[^3]: [`DjangoModelPermissions` (DRF Doc)](https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions)
[^4]: [Generating Tokens (DRF Doc)](https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens)