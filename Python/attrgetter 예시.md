---
created : 2023-03-28, Tue
topics : Operator 모듈 attrgetter 함수
context : django, python, ipython, 28032023_실습
---
# `attrgetter`
> `operator.attrgetter()` return a callable object that fetches the attribute of an object. It corresponds to specifying an attribute name like `.xxx`.

## `attrgetter` Example

Django 3.2.18
```python
todo = Todo.objects.get(pk=1)
attrgetter("pk", "content", "priority", "deadline", "created_at")(todo)
# (1, '실습 제출', 5, datetime.date(2023, 3, 28), datetime.date(2023, 3, 28))
```

정렬 함수의 key로도 자주 쓰인다고 한다.

## `itemgetter`와 차이점?
> `operator.itemgetter()` returns a callable object that fetches the item from an object. It corresponds to specifying an index like `[xxx]`.

즉, 딕셔너리나 리스트, 튜플과 같은 자료형에 `itemgetter`를 사용하고, 객체에 `attrgetter`를 사용한다.

# 참고자료
- https://note.nkmk.me/en/python-operator-usage/#get-the-attribute-of-an-object-operatorattrgetter