---
created : 2023-03-29, Wed
topics : CRUD 및 관련 메서드
context : django
---
# CREATE : 데이터 객체 생성하는 세 가지 방법
> ![[데이터 객체를 생성하는 세가지 방법]]

# READ
## `get()`
해당하는 객체 인스턴스가 1개 존재하는 경우 반환하고, 그렇지 않거나 여러개 있을 경우에는 에러를 표시한다. 따라서 고유한 값을 갖는 값으로 조회한다(ex. `pk`).
```python
Article.objects.get(pk=1)
```

`get_or_create()`도 있다.

## `filter()`
항상 `QuerySet`을 리턴한다. 존재하지 않을 경우에도 빈 `QuerySet`을 리턴한다.
```python
Article.objects.filter(title__startswith='The')
```

## `exclude()`
해당하는 레코드를 제외하고 불러온다
```python
Article.objects.filter(title__startswith='The').exclude(created_at__lt='2010-01-01')

Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello')
```

# UPDATE
## 재할당 후 저장
```python
article.title = '제목 재할당하기'
article.content = '새로운 내용'

# 추가적인 작업 후 저장
article.save()
```

## [`update()`](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update)

예시:
```python
Article.objects.filter(pk=3).update(title='new title')
```

> [!Note]
> - 데이터베이스에 바로 반영되기 때문에 추가적인 작업이 필요할 경우 사용하지 않는다.
> - 적용된 레코드 수를 반환한다.
> - [[CRUD#^1158e8|모델의 메인 테이블만 업데이트 가능하다.]]
> - `QuerySet`에만 사용할 수 있다. 데이터 객체에 바로 적용은 안됨.

예를 들어, [아래와 같은 모델](https://docs.djangoproject.com/en/3.2/topics/db/queries/#making-queries)이 있다고 하자.
```python
from django.db import models

class Blog(models.Model):
	name = models.CharField(max_length=100)
	tagline = models.TextField()

	def __str__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()

	def __str__(self):
		return self.name

class Entry(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	headline = models.CharField(max_length=255)
	body_text = models.TextField()
	pub_date = models.DateField()
	mod_date = models.DateField()
	authors = models.ManyToManyField(Author)
	number_of_comments = models.IntegerField()
	number_of_pingbacks = models.IntegerField()
	rating = models.IntegerField()

	def __str__(self):
		return self.headline
```


외래 키로 참조를 받는 `Blog` 데이터 객체의 이름을 바꾸는 첫 번째 줄은 가능하지 않지만, 참조하는 `Blog` 데이터 객체의 `id`가 1인 경우의 `Entry` 데이터 객체의 `comments_on`은 업데이트가 가능하다. ^1158e8

```python
Entry.objects.update(blog__name='foo') # Won't work!
Entry.objects.filter(blog__id=1).update(comments_on=True) # possible
```

**[[Field Lookup]]을 사용해서 참조하는 객체의 속성을 불러왔다.**

`update_or_create()`도 있다.

# DELETE
> `delete()` 메서드

```python
deleted = article.delete()
```
삭제된 총 레코드의 수와 각 객체 타입 별 몇 개가 삭제되었는지(`tuple[int, dict]`)가 반환된다. 


