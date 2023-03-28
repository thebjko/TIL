---
created : 2023-03-28, Tue
topics : Operator 모듈 attrgetter 함수
context : django, python, ipython, 28032023_실습
---
# `attergetter` Example

Django 3.2.18
```python
todo = Todo.objects.get(pk=1)
attergetter("pk", "content", "priority", "deadline", "created_at")(todo)
# (1, '실습 제출', 5, datetime.date(2023, 3, 28), datetime.date(2023, 3, 28))
```
---
# 참고자료
- https://note.nkmk.me/en/python-operator-usage/#get-the-attribute-of-an-object-operatorattrgetter