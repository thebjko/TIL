---
created_at : 2023-05-09, Tue
유효기록일 : 2023-07-23, Sun
topics : 
context : 
tags : query expression 
related : MangoPlateProject
---
# F
레코드의 값을 메모리로 불러오지 않고 DB에서 처리하기 위해 사용하는 클래스. Racing condition을 피할 수 있게 해준다.

다음은 디테일 뷰 함수이다.
```python
def detail(request, pk):
	post = Post.objects.get(pk=pk)
	...
	# 조회 발생시 조회수 증가
	post.visited = F('visited') + 1
	# 증가한 값은 다시 데이터가 로드되었을 때 반영되거나 다시 로드하지 않기 위해 다음 함수 사용
	post.refresh_from_db()
	...

```
`refresh_from_db`를 사용하지 않으면 `F('visited') + Value(1)`이 출력된다.

또는 쿼리셋을 반환하는 메서드와 `update` 메서드를 사용해 다음과 같이 구현할 수 있다:
```python
reporter = Reporters.objects.filter(name='Tintin')
reporter.update(stories_filed=F('stories_filed') + 1)
```

<br>

# Query에서 F 사용하기
한 필드의 값과 다른 필드의 값을 비교하기 위해 사용할 수도 있다/

```python
Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))
```

<br>

# With Annotation
```python
company = Company.objects.annotate(
    chairs_needed=F('num_employees') - F('num_chairs'))
```
`num_employees` 필드 값과 `num_chairs` 필드 값의 차를 구해 `chairs_needed`라는 이름의 키에 할당해 보여줄 수 있다.

<br>

# `order_by`와 함께 사용해 null 값을 가진 레코드 뒤로 보내는 예
```python
from django.db.models import F
Company.objects.order_by(F('last_contacted').desc(nulls_last=True))
```
`last_contacted`를 `order_by`와 `.desc`를 사용하고, desc 메서드의 `nulls_last` 인자로 True를 전달해 null 값을 뒤로 보낸다.

<br>

---
# 참고자료
1. https://docs.djangoproject.com/en/3.2/ref/models/expressions/
2. https://docs.djangoproject.com/en/3.2/topics/db/queries/#using-f-expressions-in-filters
3. https://docs.djangoproject.com/en/3.2/ref/models/expressions/#using-f-with-annotations
