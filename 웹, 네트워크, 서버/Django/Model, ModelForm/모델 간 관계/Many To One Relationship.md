---
created_at : <% tp.file.creation_date("YYYY-MM-DD, ddd") %>
유효기록일 : <% tp.date.now("YYYY-MM-DD, ddd") %>
topics : Many To One Relationship
context : ManyToOneRelationship 프로젝트
tags : python/django/models/relations database
related : 댓글 기능, 글, 댓글 주인 찾기
---
# Many To One Relationship

📝 참조와 역참조  
- 외래키를 사용하는 모델이 그렇지 않은 쪽을 '참조' (Comment가 Review를 참조)
- 그렇지 않은 모델이 반대쪽을 '역참조' (Review가 Comment를 역참조) 

<br>

## 참조
models.py
- `ForeignKey()` 필드 생성  
	두 개의 필수 인자
	- `to` : 어떤 모델을 참조하는가?
	- `on_delete` : 참조하는 모델 레코드(?)가 삭제되었을 때 어떻게 할건가?  
		예를 들어, Comment가 Review를 참조할 때, Review가 삭제되면, 달려 있는 Comment들은 어떻게 할건가?
		- CASCADE :  같이 삭제
		- DO_NOTHING : 아무 행동을 취하지 않음
	```python
	class Comment(models.Model):
	    review = models.ForeignKey('reviews.Review', on_delete=models.CASCADE)
	    content = models.CharField('내용', max_length=5)
	```

- 용례
	```python
	comment = Comment.objects.create(content='내용', review=Review.objects.get(pk=1))
	```

	> review 인자로 참조하는 모델의 데이터 객체 인스턴스를 전달한다.

<br>

## 역참조
- 예시 :  해당 글에 작성된 모든 댓글 조회하기
	```python
	review.comment_set.all()
	comment.objects.filter(review_id=review.pk)
	```
	> 두 코드의 SQL 쿼리문 자체는 동일하다. 하지만 첫 번째 줄은 역참조 관계를(Review -> Comment), 두 번째 줄은 참조 관계(Comment -> Review)를 나타낸다.
<br>

## `RelatedManager` 클래스[^1]
📝 일대다, 다대다 관계에서 사용하는 매니저 객체로, 두 가지 경우에 사용된다:

1. `ForeignKey` 반대편에서
	```python
	from django.db import models
	
	class Blog(models.Model):
	    # ...
	    pass
	
	class Entry(models.Model):
	    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
	```
	> `blog.entry_set` 으로 사용
	
2. `ManyToMany` 관계 양쪽에서
	```python
	class Topping(models.Model):
	    # ...
	    pass
	
	class Pizza(models.Model):
	    toppings = models.ManyToManyField(Topping)
	```
	> `toppings.pizza_set`, `pizza.toppings`로 사용
	
사용할 수 있는 메서드는 다음과 같다:
- add
- create
- remove
- clear
- set

<br>

## ManyToOneRelationship 프로젝트
> 댓글 작성 및 삭제 로직

views.py
```python
def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            '''url 및 하이퍼링크 못달게 하려면 어떤 validator를 써야되나?'''
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.save()
            return redirect('reviews:detail', review.pk)
        else:
            comment_form = CommentForm(data=request.POST)
    else:
        comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        'review': review,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)


def comment_delete(_, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', review_pk)
```
detail 함수 validation에서 comment 객체에 review 정보를 넣는 방법을 눈여겨보자.

<br>

---
# 참고자료
- Django 공식문서 v3.2

[^1]: https://docs.djangoproject.com/en/3.2/ref/models/relations/