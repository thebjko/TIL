---
created : 2023-03-30, Thu
topics : 객체 속성 확인하기
context : python, django, QuerySet API
---
> `values()` -> `QuerySet` 속성 확인  
`__dict__` -> 데이터 객체 속성 확인

> [!Caveat]  
>[[only(), defer() 메서드|only나 defer 메서드]]를 사용해 데이터를 쿼리한 경우, `__dict__` 메서드는 불러온 값의 필드를 알려주제만 `values()`는 모든 필드를 알려준다.