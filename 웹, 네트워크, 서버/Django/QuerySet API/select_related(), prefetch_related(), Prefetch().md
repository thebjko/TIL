---
created_at : 2023-05-12, Fri
유효기록일 : 2023-05-13, Sat
topics : 
context : 
tags : django QuerySet_API Prefetch optimization django-debug-toolbar
related : 
---
# `select_related()`
- 쿼리셋을 반환한다.
- 쿼리가 실행될 때 외래키 관계를 "따라가서" 해당 정보 또한 가져와 캐시한다.
- 1대 N일 때 N 쪽에서 실행한다.

<br>

### Example
```python
# DB를 조회한다.
e = Entry.objects.get(id=5)

# Hits the database again to get the related Blog object.
b = e.blog
```
이 경우 DB를 두번 조회하지만 `selected_related` 로 조회하는 아래의 경우
```python
# Hits the database.
e = Entry.objects.select_related("blog").get(id=5)

# Doesn't hit the database, because e.blog has been prepopulated
# in the previous query.
b = e.blog
```

`e.blog`가 DB를 다시 조회하지 않는다. 이미 관련 정보가 `select_related`를 통해 캐시에 저장되었기 때문이다.

메서드 체인의 순서는 중요하지 않다. 아래 두 쿼리는 동일한 결과를 갖는다. 
```python
Entry.objects.filter(pub_date__gt=timezone.now()).select_related("blog")
Entry.objects.select_related("blog").filter(pub_date__gt=timezone.now())
```

<br>

### Example #2
```python
from django.db import models


class City(models.Model):
    # ...
    pass


class Person(models.Model):
    # ...
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class Book(models.Model):
    # ...
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
```
위 경우에서 아래와 같이 `id`가 4인 Book 인스턴스의 저자의 고향 정보를 불러올 수 있다.
```python
# DB에서 id가 4인 책의 저자와 고향 정보까지 같이 불러온다(join).
b = Book.objects.select_related("author__hometown").get(id=4)
p = b.author  # DB를 조회하지 않는다.
c = p.hometown  # DB를 조회하지 않는다.

# select_related()를 사용하지 않으면...
b = Book.objects.get(id=4)  # DB를 조회한다.
p = b.author  # DB를 조회한다.
c = p.hometown  # DB를 조회한다.
```

<br>

### Caveat
- `ForeignKey`나 `OneToOneField` 참조관계를 `select_related()` 메서드에 전달할 수 있다. (여러개 가능?)
- 반대 방향으로도 참조가 가능하다. `related_name`에 인수로 전달된 값으로 호출할 수 있다. 관계가 복잡해질 경우 유용할 것 같다.
	```python
	Book.objects.select_related("author").select_related("book_set__author"). ... 왜?
	```
- `select_related()` 메서드에 인수로 아무것도 전달하지 않을수도 있다. 이 경우 null이 아닌 외래키를 따라가 정보를 캐시한다. null이 가능할 경우 어떤 외래키를 따라갈지 반드시 명시해야한다. 공식 문서는 이 방법을 권장하지 않는다. 쿼리가 더 복잡하고 필요한 데이터보다 더 많은 데이터를 반환하기 때문이다. (메모리 비용 증가)
- `None`을 인수로 전달하면, 이전에 불러와 캐시했던 정보들을 초기화 할 수 있다.
	```python
	without_relations = queryset.select_related(None)
	```
- Chaining에 관하여 - 아래 두 방법은 동일하다.
	```python
	select_related('foo', 'bar')
	select_related('foo').select_related('bar')
	```

<br>

# `prefetch_related()`
조회시 관계로 연결된 DB에서 정보를 같이 가져와 반환한다. 많은 경우 `IN` 을 사용하는 SQL 쿼리문과 같다.

<br>

### `select_related()` 메서드와 비슷한점, 차이점?
DB 쿼리를 줄인다는 점에서 비슷한 목적을 가지고 있지만, 전략이 다르기 때문에 사용되는 경우가 다르다.

`select_related` 메서드는 `SQL JOIN`을 사용해 연관된 객체의 필드를 `SELECT` 문에 포함함으로 동작한다. 이러한 이유로 `select_related` 메서드는 한 쿼리에서 요청된 정보를 모두 가져온다. 너무 많은 정보를 가져오는걸 피하기 위해 `select_related` 메서드는 `ForeignKey`나 `OneToOneRelationship`과 같은 1대 N, 1대 1 관계에서만 사용할 수 있도록 제한되어있다.

반면 `prefetch_related` 메서드는 각 관계당 따로 조회를 실시하고, 파이썬의 'joining'을 실시한다. 이러한 전략이 (1대 1, 1대 다 관계 +) 다대다, 다대 1 관계에서 데이터를 'prefetch' 할 수 있게 한다. (fetch는 가져오다는 뜻. 즉 미리 가져온다는 의미.)  `GenericRelation`과 `GenericForeignKey` 또한 prefetch 할 수 있게 한다는데, 지금은 넘어가기로 하자. 

참고할 자료:
- https://stackoverflow.com/questions/65278332/django-tutorial-reverse-for-results-with-arguments-1-not-found-error
- https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm

<br>

### Example
```python
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=30)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )
        
```
위와 같은 모델에서 다음과 같이 조회한다고 하자
```python
>>> Pizza.objects.all()
["Hawaiian (ham, pineapple)", "Seafood (prawns, smoked salmon)"...
```

이 경우 Pizza 모델의 `__str__` 메서드가 실행될 때마다 `self.toppings.all()`로 DB를 조회한다는 문제가 있다. 반환된 `QuerySet`의 모든 원소에 대해 DB를 조회하는 것이다. 하지만 아래와 같이 `prefetch_related` 메서드를 사용하면 쿼리를 2번으로 줄일 수 있다.
```python
>>> Pizza.objects.prefetch_related('toppings')
```

이 경우 `__str__` 메서드가 실행되면서 `self.toppings.all()` 쿼리문이 실행될 때 DB를 조회하지 않고 `prefech_related` 메서드가 가져온 캐시를 조회해 효율을 높일 수 있다. 첫 번째 단계에서 쿼리한 정보를 모두 가져와 캐시하고, "the additional queries in `prefetch_related()` are executed after the QuerySet has begun to be evaluated and the primary query has been executed."

만약 모델 인스턴스로 이루어진 순회할 수 있는 객체가 있는 경우 `prefetch_related_objects()`를 사용할 수 있다.

*캐시는 메모리에서 이루어지기 때문에, 해당 정보가 필요한 시점에 수행하도록 하자.*  

아래와 같이 `cache_clear()` 메서드를 사용하면 캐시를 비울 수 있다.

```python
my_queryset = MyModel.objects.prefetch_related('related_model')
```

```python
# Django 3.2 이전
from django.core.cache import cache

cache_key = my_queryset._cache_key()
cache.delete(cache_key)


# Django 3.2 이상
my_queryset.cache_clear()
```

<br>

### 📝 Note
여느 `QuerySet`과 마찬가지로, 다른 DB 쿼리를 의미하는 메서드를 이어서 호출하면, 이전에 캐시되었던 결과는 무시되고 새로운 DB 쿼리 결과를 가져온다. 예를 들어
```python
>>> pizzas = Pizza.objects.prefetch_related('toppings')
>>> [list(pizza.toppings.filter(spicy=True)) for pizza in pizzas]
```
첫 번째 줄에서 pizzas는 각 Pizza 인스턴스에 대해 `pizza.toppings.all()`의 결과를 미리 가져왔다. 하지만 pizzas에 대해 순회하며 각 값에 `.toppings.filter(spict=True)`라고 다시 메서드를 실행하면 이전에 가져와 캐시로 저장된 `pizza.toppings.all()`는 무시된다. (그럼 어떡해야되지? 어떡해야 각 pizza에 저장된 topping들을 활용할 수 있지?)

또한 DB에 저장된 값을 바꾸는 메서드인 `add()`, `remove()`, `clear()`, `set()`을 `related_manager`에 사용하면, prefetch해 캐시에 저장된 값들은 초기화된다.

<br>

### JOIN 여러번 하기
```python
class Restaurant(models.Model):
    pizzas = models.ManyToManyField(Pizza, related_name="restaurants")
    best_pizza = models.ForeignKey(
        Pizza, related_name="championed_by", on_delete=models.CASCADE
    )
    
```
이 경우 아래와 같이 참조 관계를 2번 타고 prefetch 할 수 있다. 
```python
>>> Restaurant.objects.prefetch_related("pizzas__toppings")
```
Restaurant → Pizza → Topping : 각 단계별 한개씩 총 3개의 쿼리로 조회 결과를 가져올 수 있다.

```python
>>> Restaurant.objects.prefetch_related("best_pizza__toppings")   # 3개 쿼리
>>> Restaurant.objects.select_related("best_pizza").prefetch_related("best_pizza__toppings")   # 2개 쿼리
```
`select_related`를 조합해 쿼리 수를 줄일 수 있다(Restaurant + Pizza → Topping). 위에서 설명했듯 `select_related` 메서드는 한번의 쿼리에 모든 결과를 가져오지만 1대 1 또는 1대 다 관계일 경우에만 사용가능하다.

⭐️ 그리고 이 경우 `prefetch_related` 단계에서 `select_related`가 가져온 `best_pizza` 객체들을 탐지해 이 단계를 다시 반복하지 않는다.

`select_related`와 마찬가지로 체이닝 규칙이 적용되어 조회 결과를 누적할 수 있고, 이전 `prefetch_related`를 초기화하기 위해서 `None`을 인수로 전달한다.

<br>

# `Prefetch()` : prefetch 커스텀하기
`prefetch_related`의 인수로 사용되며, 좀 더 세세한 컨트롤을 가능하게 한다.
```python
>>> from django.db.models import Prefetch
>>> Restaurant.objects.prefetch_related(Prefetch('pizzas__toppings'))
```

쿼리셋의 디폴트 순서를 바꾸기 위해서도 사용할 수 있다.
```python
>>> Restaurant.objects.prefetch_related(
...     Prefetch('pizzas__toppings', queryset=Toppings.objects.order_by('name'))
... )
```
'name'을 기준으로 오름차순 정렬된 쿼리셋을 가지고 prefetch를 수행한다.

비교하자면, 다음과 같은 코드는 ~~실행해보진 않았지만~~ topping의 name을 기준으로 Restaurant을 정렬하고 있다.
```python
>>> Restaurant.objects.prefetch_related('pizzas__toppings').order_by('pizzas__toppings__name')
```

또한 [[select_related(), prefetch_related(), Prefetch()#📝 Note|위에서 풀지 못했던 문제]]의 답도 될 수 있을 것 같다. **아직 확인하지 않음.**
```python
>>> pizzas = Pizza.objects.prefetch_related(
...     Prefetch('toppings', queryset=Toppings.objects.filter(spicy=True))
... )
>>> [list(pizza.toppings.filter(spicy=True)) for pizza in pizzas]   # 확인 필요!!!
>>> [list(pizza.toppings.all()) for pizza in pizzas]
```
이 경우 각 Pizza 인스턴스에 대해 `pizza.toppings.filter(spicy=True)`가 캐시되어 있어 활용할 수 있을 거라고 **추측**해본다.

또, `select_related()`를 `Prefetch` 안에 사용해 쿼리의 수를 더 줄일 수 있다.
```python
>>> Pizza.objects.prefetch_related(
...     Prefetch('restaurants', queryset=Restaurant.objects.select_related('best_pizza'))
... )
```

<br>

### `to_attr`
`to_attr` 인자를 사용해 prefetch한 값들을 저장할 수도 있다.
```python
>>> vegetarian_pizzas = Pizza.objects.filter(vegetarian=True)
>>> Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', to_attr='menu'),
...     Prefetch('pizzas', queryset=vegetarian_pizzas, to_attr='vegetarian_menu')
... )
```
`'menu'`에 모든 Pizza를 저장했고, `vegetarian_pizzas`를 사용한 prefetch는 `'vegetarian_menu'`에 저장했다.
```python
>>> vegetarian_pizzas = Pizza.objects.filter(vegetarian=True)
>>> Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', queryset=vegetarian_pizzas, to_attr='vegetarian_menu'),
...     'vegetarian_menu__toppings')
```
위와 같이 `vegetarian_menu`의 `toppings`까지 prefetch할 수 있다.
```python
>>> queryset = Pizza.objects.filter(vegetarian=True)
>>>
>>> # Recommended:
>>> restaurants = Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', queryset=queryset, to_attr='vegetarian_pizzas'))
>>> vegetarian_pizzas = restaurants[0].vegetarian_pizzas
>>>
>>> # Not recommended:
>>> restaurants = Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', queryset=queryset))
>>> vegetarian_pizzas = restaurants[0].pizzas.all()
```

가져온 값을 더 깊이 필터링 해야될 경우 `to_attr`을 사용해 의미를 더 명확히 할 수 있다.

<br>

### 커스텀 prefetcing이 유용한 경우들
1대 1, 1대 N의 경우 보통 `select_related`를 사용하지만 커스텀 prefetching이 유용한 경우들이 있다.
- 더 깊이 prefetch 하고싶을 경우
- 관련 객체들의 subset만 가져오고 싶을 경우
- [[only(), defer() 메서드|deferred fields]]와 같이 성능 최적화 기법을 사용하고 싶을 경우
```python
>>> queryset = Pizza.objects.only('name')
>>>	
>>> restaurants = Restaurant.objects.prefetch_related(
...     Prefetch('best_pizza', queryset=queryset)
... )
```

DB 선택 :  여러 DB를 사용중일 경우 using 메서드를 사용한다. (다른 DB를 어떻게 참조하지?)
```python
>>> # Both inner and outer queries will use the 'replica' database
>>> Restaurant.objects.prefetch_related("pizzas__toppings").using("replica")
>>> Restaurant.objects.prefetch_related(
...     Prefetch("pizzas__toppings"),
... ).using("replica")
>>>
>>> # Inner will use the 'replica' database; outer will use 'default' database
>>> Restaurant.objects.prefetch_related(
...     Prefetch("pizzas__toppings", queryset=Toppings.objects.using("replica")),
... )
>>>
>>> # Inner will use 'replica' database; outer will use 'cold-storage' database
>>> Restaurant.objects.prefetch_related(
...     Prefetch("pizzas__toppings", queryset=Toppings.objects.using("replica")),
... ).using("cold-storage")
```

<br>

### 📝 Note
**조회(lookup) 순서에 주의하자.**
```python
>>> prefetch_related('pizzas__toppings', 'pizzas')
```
이 경우 첫 번째 조회에서 pizzas를 조회하는데 두 번째에 다시 조회하고 있다.

```python
>>> prefetch_related('pizzas__toppings', Prefetch('pizzas', queryset=Pizza.objects.all()))
```
첫 번째 조회에서 pizzas를 조회했는데, 두 번째 `Prefetch` 내부에서 pizzas를 조회할 쿼리셋을 다시 지정하고 있다. 이 경우는 `ValueError`를 발생시킨다. 먼저 실행된 조회에 사용된 쿼리셋을 변경하고 있기 때문이다. 

```python
>>> prefetch_related('pizza_list__toppings', Prefetch('pizzas', to_attr='pizza_list'))
```
첫 번째 조회에서 `pizza_list`가 아직 존재하지 않다. 두 번째에서야 `to_attr`을 통해 만들어지기 때문이다. 이 경우는 `AttributeError`가 발생한다.

<br>

---
# 참고자료
- https://wave1994.tistory.com/70
- https://leffept.tistory.com/312
- https://velog.io/@rosewwross/Django-selectrelated-%EC%99%80-prefetchedrelated%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B0%B8%EC%A1%B0
- https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-related
- https://docs.djangoproject.com/en/4.2/ref/models/querysets/#prefetch-related


[^1]: 
