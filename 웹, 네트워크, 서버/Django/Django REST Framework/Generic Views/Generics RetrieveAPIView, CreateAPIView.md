---
created_at : 2023-04-27, Thu
유효기록일 : 2023-04-28, Fri
topics : 
context : 
tags : python/django/rest_framework generic_views
related : 
---
DRF는 Django의 View 클래스를 상속하는 APIView 클래스를 제공한다. 다른 메서드를 제공한다는 점을 제외하고 View 클래스처럼 사용할 수 있다. Generics 뷰는 좀 더 특화된 목적을 위해 사용한다. 

> 처음에는 뷰함수만 있었다고 한다. 그러다 뷰 함수들에 어떤 패턴이 있다는 걸 알게 되었고, 이런 패턴들을 추상화시켜 Function-based Generic View가 탄생하게 되었다. 그런데 실제로 사용되는 특별한 목적을 위해 기능을 확장하거나 커스터마이즈 하는데 있어 한계에 다랐고, Class-based Generic View가 탄생하게 된다. 

REST Framework Class-Based Generic View들은 GenericAPIView와 Mixin을 사용해 각 용도에 맞는 Generic View로 섞어낸다. 

<br>

# Generics RetrieveAPIView
Used for **read-only endpoints** to represent a single model instance.  RetrieveModelMixin과 GenericAPIView 클래스를 상속한다. Endpoint로 호출해 정보를 읽기 위한 detail 뷰와 같다. GET 메서드 핸들러를 제공한다. 이 메서드는 Response를 반환하는 RetrieveModeMixin의 retrieve 메서드를 호출한다. 

```python
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'   # default

product_detail_view = ProductDetailAPIView.as_view()
```
pk가 필요하기때문에 urls.py에서 variable routing으로 전달하는데, `lookup_field`에 할당된 값을 사용한다. 기본값은 'pk'.

```python
# products/urls.py

urlpatterns = [
    path('', views.product_create_view),
    path('<int:pk>/', views.product_detail_view),   # pk가 위 ProductDetailAPIView로 전달된다.
]
```

<br>

# GenericsCreateAPIView
Used for **create-only endpoints**. CreateModelMixin와 GenericAPIView를 상속한다. POST 메서드 핸들러를 제공한다. 지정된 endpoint에 아래와 같이 post 메서드로 호출하면 요청한 title과 price를 갖는 데이터가 생성된다.
```python
import requests

endpoint = "http://localhost:8000/api/products/"

data= {
    "title": "This field is done.",
    "price": 32.99,
}
get_response = requests.post(endpoint, json=data)
print(get_response.json())
```

CreateModelMixin에는 `perform_create`라는 메서드가 있는데, create 메서드가 호출될 때에 실행되며, serializer를 저장한다. 

```python
	 def perform_create(self, serializer):
        """
        Assign something to the data(json 인자로 넘어온).
        CreateModelMixin의 perform_create는 serializer.save() 실행.
        """
        print(serializer.validated_data)   # validation 통과한 데이터만 출력(OrderedDict)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content)
        # super().perform_create(serializer)
        # send a Django signal (어떻게 어떤 signal을?)
```
여기서 serializer를 저장하기 전에, 다른 필드에 대해 전처리를 수행할 수 있다. 위 예시에서는 content를 제공하지 않았을 때 content에 다른 값을 할당하고 save 메서드에 넘겨서 content가 title과 같은 값을 가지도록 처리했다.

CreateAPIView는 post 메서드를 가지고 있고, CreateModelMixin의 create 메서드를 실행한 결과를 리턴한다. create 메서드는 Response를 반환한다. Endpoint가 호출될 때 이 post가 실행되나보다. 

<br>

"Using Function Based Views For Create Retrieve or List"까지 듣고 정리 → 아니다
위에 Django 분석하고 푸시하자.

---
# 참고자료
- [CodingEntrepreneurs](https://youtu.be/c708Nf0cHrs)
- https://www.django-rest-framework.org/api-guide/views/
- https://stackoverflow.com/questions/67476659/generic-views-vs-apiview-vs-viewsets-vs-modelviewsets
- https://www.django-rest-framework.org/api-guide/generic-views/#createmodelmixin
- [The relationship and history of generic views, class-based views, and class-based generic views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/intro/#the-relationship-and-history-of-generic-views-class-based-views-and-class-based-generic-views)
- 

[^1]: