---
created_at : 2023-04-26, Wed
유효기록일 : 2023-04-26, Wed
topics : 
context : serializer
tags : python/django/rest_frame
related : 
---
# SerializerMethodField

products/models.py
```python
from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)

    @property
    def sale_price(self):
        return f"{float(self.price) * .8:.2f}"
    
    def get_discount(self):
        return "122"
```
`@property` 데코레이터로 `sale_price`를 속성으로 만든다. 임의의 값을 반환하는 `get_discount`라는 메서드를 만든다. 

products/serializers.py
```python
from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title',
            'content',
            'price',
            'sale_price',
            'get_discount',
        )

```
`ProductSerializer`에서 다음과 같이 `get_discount`를 필드에 넣으면 다음과 같이 잘 반환된다.
```
{'title': 'hello world again', 'content': 'this is amazing', 'price': '1.00', 'sale_price': '0.80', 'get_discount': '122'}
```
그런데 아래와 같이 변경한 뒤 API를 호출하면
```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title',
            'content',
            'price',
            'sale_price',
            'get_discount',
            'my_discount',
        )
```
다음과 같은 예외가 발생한다.
```
django.core.exceptions.ImproperlyConfigured: Field name `my_discount` is not valid for model `Product`.
```

`SerializerMethodField` 필드를 추가하면
```python
class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = (
            'title',
            'content',
            'price',
            'sale_price',
            'get_discount',
            'my_discount',
        )
```
```
AttributeError: 'ProductSerializer' object has no attribute 'get_my_discount'
```
라는 예외로 바뀐다. `ProductSerializer`에 `get_my_discount` 속성(메서드)을 만들어서 해결.

```python
class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = (
            'title',
            'content',
            'price',
            'sale_price',
            'get_discount',
            'my_discount',
        )
    
    def get_my_discount(self, obj):
        return obj.get_discount()
```
`get_my_discount` 메서드는 obj로 데이터 인스턴스(`model = Product`)를 받아 객체에 담긴 `get_discount` 메서드를 실행하는 시리얼라이저의 메서드이다. 단순히 반환하는 것 뿐만 아니라 다른 연산을 하도록 설계할 수도 있다.

위와 같이 간단히 필드 이름을 바꿀 수 있는게 DRF를 사용하는 이유 중 하나라고 한다. 이 외에도 다른 기능들이 많이 있다고 한다.

<br>

## Caveat
다음은 `SerializerMethodField`의 메서드이다. 필드 이름과 `get_`을 결합해 메서드 이름을 만든다. 정확히 어떤 원리로 동작하는지 설명할 수는 없지만 필드 이름과 serializer 메서드 이름의 관계를 유추해볼 수 있다.

fields.py
```python
	def bind(self, field_name, parent):
        # The method name defaults to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = 'get_{field_name}'.format(field_name=field_name)

        super().bind(field_name, parent)

	 def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)
```

공식 문서에서도 `SerializerMethodField`의 `method_name` 인자로 아무 값도 주어지지 않으면 `get_{필드 이름}`을 메서드로 사용한다고 한다.

<br>

---
# 참고자료
- [CodingEntrepreneur - Django Rest Framework Model Serializers](https://youtu.be/c708Nf0cHrs)
- [DRF 공식문서](https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield)

[^1]: