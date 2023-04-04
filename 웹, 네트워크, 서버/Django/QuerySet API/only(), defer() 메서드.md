---
created : 2023-03-29, Wed
topics : QuerySet API only(), defer() method
context : django QuerySet API
---
# `only()`와 `defer()`
> 필요한 속성만 db에서 바로 불러오는 방법을 찾아보다가 보게 된 메서드. 원하는 필드에 대해서만 쿼리를 실행하기 때문에 쿼리 비용을 줄일 수 있다. `QuerySet` 객체를 반환한다.


## `defer()`
`defer()` 예시:
```python
In [9]: account = AccountBook.objects.defer('id', 'created_at')

In [10]: account[0].__dict__
Out[10]: 
{'_state': <django.db.models.base.ModelState at 0x105d51010>,
 'id': 4,
 'note': 'sad',
 'description': 'w',
 'category': 'asd',
 'amount': 0,
 'date': datetime.date(2023, 3, 23),
 'updated_at': datetime.datetime(2023, 3, 31, 2, 25, 54, 107203, tzinfo=<UTC>)}
```
> 'created_at' 필드의 값들을 가져오지 않는다.

`defer` 메서드의 인자로 `'id'`를 전달했음에도 출력되었다. `only()`와 `defer()` 메서드는 항상 `id`를 가져온다.

- chaining이 가능하다. 이미 `defer` 메서드가 호출된 쿼리셋은 그 상태로 남아있는다.
	```python
	AccountBook.objects.defer('created_at').defer('updated_at')
	
	# equivalently
	AccountBook.objects.defer('created_at', 'updated_at')
	
	```

- 메서드 인자로 `None`을 주면 초기화가 가능하다.
	```python
	a = AccountBook.objects.defer('created_at', 'updated_at')
	b = a.defer(None)

	b.__dict__

	# 출력
	{'_state': <django.db.models.base.ModelState at 0x1061d9c10>,
	 'id': 4,
	 'note': 'sad',
	 'description': 'w',
	 'category': 'asd',
	 'amount': 0,
	 'date': datetime.date(2023, 3, 23),
	 'created_at': datetime.datetime(2023, 3, 31, 2, 25, 54, 107203, tzinfo=<UTC>),
	 'updated_at': datetime.datetime(2023, 3, 31, 2, 25, 54, 107203, tzinfo=<UTC>)}
	```


## `only()`
> `defer()` 메서드와 다른 점을 중심으로 다룬다.

`only()` 예시:
```python
account = AccountBook.objects.only('created_at', 'updated_at').only('note')
```
위의 경우 맨 마지막에 호출된 `only()` 메서드만 효력을 발휘한다. 위 코드는 데이터베이스에서 `'note'` 필드에 대한 값만 가져온다. "`defer()` acts incrementally, `only()` replaces the set of fields to load immediately"

## 조합
```python
# "headline", "body" 필드 중 "body"를 defer -> "headline"만 가져온다
Entry.objects.only("headline", "body").defer("body")

# 마지막 only 메서드가 이전 세트 필드들을 대체하기 때문에 "headline"과 "body"만 가져온다
Entry.objects.defer("body").only("headline", "body")
```


## 주의사항
- `defer()` 메서드를 사용해 생성된 객체를 `save()`한다면 불려진 필드만 저장된다.
- Advanced use-cases를 위한 메서드라고하면서 가급적 `only()`는 자제하고, 쓰지 않는게 확실한 필드를 불러오지 않기 위한 `defer()` 메서드를 사용하라고 한다. 그리고 자주 이 메서드를 사용한다면 자주 사용하지 않는 필드들을 다른 테이블로 옮겨 DB를 [[DB 정규화|정규화]] 하기를 권장한다. 만약 이 항목들이 반드시 같은 테이블에 있어야 한다면, `Meta.managed = False`로 모델을 만들라고 한다 -> 가독성을 높이고 메모리를 덜 사용하게 함

---
# 참고자료
- [Django 공식문서](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#defer)