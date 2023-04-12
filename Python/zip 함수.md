---
created_at : 2023-04-12, Wed
유효기록일 : 2023-04-12, Wed
topics : 
context : 
tags : python/built-in/functions
related : 제너레이터와 이터레이터
---
# zip
- 튜플 이터레이터를 반환
- 인수가 없으면 empty iterator를 반환, 하나일 경우 1 튜플 이터레이터를 반환
- is lazy : The elements won’t be processed until the iterable is iterated on, e.g. by a for loop or by wrapping in a list.
- 길이가 다른 이터러블을 zip 하려면 `itertools.zip_longest()` 사용

```python
>>> a = zip(*[range(10)]*5, strict=True)
>>> for i in a:
...     print(i)
...
(0, 0, 0, 0, 0)
(1, 1, 1, 1, 1)
(2, 2, 2, 2, 2)
(3, 3, 3, 3, 3)
(4, 4, 4, 4, 4)
(5, 5, 5, 5, 5)
(6, 6, 6, 6, 6)
(7, 7, 7, 7, 7)
(8, 8, 8, 8, 8)
(9, 9, 9, 9, 9)
```

-  `strict` 인자를 True로 지정하면 zip 함수에 인수로 넘겨진 이터러블 중 하나가 먼저 소진될 경우 `ValueError`를 raise한다.[^1] (버전 3.10에서 추가됨)
	```python
    >>> a = [1,2,3,4,5]
    >>> b = [1,2,3,4]
    >>> for i in zip(a, b, strict=False):
	...     print(i)
	...
	(1, 1)
	(2, 2)
	(3, 3)
	(4, 4)
	
	>>> for i in zip(a, b, strict=True):
    ...     print(i)
    ...
	(1, 1)
	(2, 2)
	(3, 3)
	(4, 4)
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	ValueError: zip() argument 2 is shorter than argument 1
	```

---
# 참고자료
- https://docs.python.org/ko/3/library/functions.html?highlight=zip#zip
- https://stackoverflow.com/questions/32954486/zip-iterators-asserting-for-equal-length-in-python

[^1]: https://peps.python.org/pep-0618/