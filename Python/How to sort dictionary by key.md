---
created : 2023-03-27, Mon
topics : sort, dictionary
context : python
---
# [How to sort dictionary by key](https://stackoverflow.com/a/47017849)

1. 파이썬 버전 3.7 부터 아래와 같은 syntax 사용 가능
    ```python
    >>> d = {2:3, 1:89, 4:5, 3:0}
    >>> dict(sorted(d.items()))
    {1: 89, 2: 3, 3: 0, 4: 5}
    ```

2. `collections` 모듈의 `OrderedDict` 클래스 사용
    ```python
    >>> from collections import OrderedDict
    >>> d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}
    
    >>> OrderedDict(sorted(d.items(), key=lambda t: t[0]))
    OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])
    
    >>> OrderedDict(sorted(d.items(), key=lambda t: t[1]))
    OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])
    ```
