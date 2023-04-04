---
created : 2023-03-26, Sun
topics : 파이썬 리스트의 성질
context : python
---
# 리스트의 성질
1. 슬라이싱에는 인덱스에러가 나지 않는다.
	```python
	>>> ls = [*range(1, 11)]
	>>> ls[20:30]
	[]
	```

2. 슬라이싱을 통해 접근한 값의 타입은 항상 리스트이다.
	```python
	>>> ls = [*range(1, 11)]
	>>> ls[:1]
	[1]
    ```

3. `heapq`를 `copy`하면 `heapq`이다.
	```python
	>>> import heapq as hq
    >>> ls = [(4,3), (2,5), (5,7)]
    >>> ls
	[(4, 3), (2, 5), (5, 7)]
    >>> hq.heapify(ls)
    >>> ls
	[(2, 5), (4, 3), (5, 7)]
    >>> l = ls[:]
    >>> l
	[(2, 5), (4, 3), (5, 7)]
    >>> hq.heappop(l)
	(2, 5)
	```