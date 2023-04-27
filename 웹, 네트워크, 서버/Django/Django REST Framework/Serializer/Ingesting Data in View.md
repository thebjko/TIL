---
created_at : <% tp.file.creation_date("YYYY-MM-DD, ddd") %>
유효기록일 : <% tp.date.now("YYYY-MM-DD, ddd") %>
topics : 
context : 
tags : python/django/rest_framework
related : validation
---
# Ingesting Data in View

```python
# products/views.py

@api_view(["GET", "POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # instance = serializer.save()   # Product object. save 했을때와 하지 않았을 때 리턴값이 다르다.
        # save 하지 않으면 not based off of Model, else based off of only serializer
        # save 하지 않으면 데이터 인스턴스가 생성되지 않아 get_my_discount 메서드에 obj가 전달되지 않는다.
        print(serializer.data)   
        return Response(serializer.data)
    return Response({"some data": "exception"}, status=400)
```
serializer의 save 메서드는 Product 객체를 생성한다. 그래서 이 때 `serializer.data`는 serializer의 모든 필드 값에 대한 데이터를 담고 있다. 하지만 save하지 않으면 데이터 인스턴스가 생성되지 않아 입력한 값과 serializer에 있는 `get_my_discount`만 반환하게 된다.

저장되지 않았을 때 아래의 코드로 요청해보자:
```python
# py_client/basic.py

import requests

endpoint = "http://localhost:8000/api/"

get_response = requests.get(endpoint, params={"abc": 123}, json={'title': 'Hello world'})
print(get_response.json())
```
출력값은 아래와 같다.
```python
{'title': 'Hello world', 'content': None, 'my_discount': None}
```

`serializer.save()` 후 같은 요청을 보낸다면 아래와 같은 출력을 얻을 수 있다. Model이 제공하는 모든 데이터를 serializer를 통해 전달받을 수 있다.
```python
{'title': 'Hello world', 'content': None, 'price': '99.99', 'sale_price': '79.99', 'get_discount': '122', 'my_discount': '122'}
```
`my_discount` 함수는 인스턴스가 저장이 되었을 때에만 obj로 해당 객체를 전달받을 수 있다. 그래서 아래와 같이 처리했다.
```python
# products/serializers.py

def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        # if not isinstance(obj, Product):
        #     return None
        return obj.get_discount()
```
주석처리한 부분으로도 예외처리를 할 수 있다. 이 방법으로는 어떤 유형의 객체여야 하는지 명시할 수 있다.

title은 모델 필수 입력값이기 때문에 json으로 title을 반드시 전달해야 한다. 그렇지 않으면 validation에 실패하고 예외처리된다.

<br>

---
# 참고자료
- [CodingEntrepreneurs](https://youtu.be/c708Nf0cHrs)

[^1]: