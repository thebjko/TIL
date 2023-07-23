---
created_at : 2023-04-07, Fri
유효기록일 : 2023-07-23, Sun
topics : 
context : 
tags : python itertools.chain
related : 
---
# `itertools.chain`
이 메서드는 각 리스트를 순회하면서 다른 빈 리스트에 `append`하는 것 보다 훨씬 성능이 좋다.

```python
from itertools import chain
from operator import attrgetter


result_list = list(chain(page_list, article_list, post_list))

# attrgetter를 사용해 순서 정하기
result_list = sorted(
    chain(page_list, article_list, post_list),
    key=attrgetter('date_created')
)
```

---
# 참고자료
- https://stackoverflow.com/questions/431628/how-to-combine-multiple-querysets-in-django

[^1]: