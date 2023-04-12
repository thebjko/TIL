---
created_at : 2023-04-12, Wed
유효기록일 : 2023-04-12, Wed
topics : 
context : 이터레이터, 제너레이터
tags : python/functions/built-in
related : 
---
# `iter()`
> `iter(obejct)`  
> `iter(object, sentinel)`

- 이터레이터 객체를 반환.
- 두 번째 인수가 없다면 첫 번째 인수는 무조건 iterable protocol(`__iter__` 메서드) 또는 sequence protocol(`__getitem__` 메서드)을 지원하는 객체여야 한다. 그렇지 않으면 `TypeError`를 발생시킨다. 
- Sentinel이라고 불리는 두 번째 인수가 있다면, 첫 번째 인수는 [[callable object|콜러블 객체]]여야 한다. `__next__` 메서드가 실행 될 때마다 첫 번째 인수로 넘겨진 콜러블 객체를 호출한다. 그로부터 sentinel과 같은 값이 반환될 때 `StopIteration` 예외를 발생시킨다. 그 전까지는 콜러블 객체에서 반환된 값을 반환한다.

# `next()`
> `next(iterator)`  
> `next(iterator, default)`

- 이터레이터에서 다음 아이템을 가져온다.
- 디폴트 값이 있으면 이터레이터가 소진되었을 때 이 값이 반환되지만 없다면 `StopIteration` 예외를 발생시킨다.



---
# 참고자료
- https://docs.python.org/3/library/functions.html#iter
- https://docs.python.org/3/library/functions.html#next

[^1]: