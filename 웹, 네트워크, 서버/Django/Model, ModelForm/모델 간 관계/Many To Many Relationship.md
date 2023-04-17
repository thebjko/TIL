---
created_at : 2023-04-17, Mon
유효기록일 : 2023-04-17, Mon
topics : Many To Many Relationship
context : 
tags : python/django/models/relations database related_name
related : 
---
# Many To Many Relationship
1. 중개 모델(Intermediate Model) 사용하기
	```python
	class Doctor(models.Model):
	    name = models.TextField()
	
	    def __str__(self):
	        return f'{self.pk}번 의사 {self.name}'
	
	
	class Patient(models.Model):
	    name = models.TextField()
	
	    def __str__(self):
	        return f'{self.pk}번 환자 {self.name}'
	        
	
	class Reservation(models.Model):
	    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	
	    def __str__(self):
	        return f'{self.doctor_id}번 의사의 {self.patient_id}번 환자'
	```
	Doctor 모델과 Patient 모델을 Reservation이라는 관계로 묶었다. Reservation 모델(테이블)은 각 레코드에 pk, doctor_id, patient_id를 갖는다. Doctor와 Reservation은 1:N이고, Patient 또한 Reservation 테이블과 1:N 관계를 갖는다. Reservation의 매니저를 호출해 레코드를 생성한다(ex. `Reservation.objects.create(...)`).

2. ManyToManyField 사용
	```python
	from django.db import models
	
	
	class Doctor(models.Model):
	    name = models.TextField()
	
	    def __str__(self):
	        return f'{self.pk}번 의사 {self.name}'
	
	
	class Patient(models.Model):
	    # ManyToManyField 작성
	    doctors = models.ManyToManyField(Doctor)
	    name = models.TextField()
	
	    def __str__(self):
	        return f'{self.pk}번 환자 {self.name}'
	```
	Reservation 모델을 빼고 대신 Patient 모델에 doctors(ManyToManyField) 필드를 만든다. 여전히 중개 테이블이 만들어진다(hospitals_patient_doctors). RelatedManager를 사용해 중개 테이블에 레코드를 작성할 수 있다. 예를 들어 `Doctor.patient_set` 또는 `Patient.doctors`로 호출하며, 사용할 수 있는 메서드는 다음과 같다:
	- add : 새로운 레코드 생성. 관계지어진 모델 오브젝트 셋(related object set)에 지정한 모델 오브젝트를 추가한다.
	- create : add와 같지만 새로 만들어진 객체를 리턴한다.
	- remove: 지정한 오브젝트 삭제
	- clear : related object set에서 모든 객체를 삭제한다
	- set : *Replace* the set of related objects
		```python
        >>> new_list = [obj1, obj2, obj3]
        >>> e.related_set.set(new_list)
		```

3. 진료 차트에 다른 필드가 있다면, 중개 모델을 직접 작성해야한다.
	```python
	from django.db import models
	
	
	class Doctor(models.Model):
	    name = models.TextField()
	
	    def __str__(self):
	        return f'{self.pk}번 의사 {self.name}'
	
	
	class Patient(models.Model):
	    doctors = models.ManyToManyField(Doctor, through='Reservation')
	    name = models.TextField()
	
	    def __str__(self):
	        return f'{self.pk}번 환자 {self.name}'
	
	
	class Reservation(models.Model):
	    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	    symptom = models.TextField()
	    reserved_at = models.DateTimeField(auto_now_add=True)
	
	    def __str__(self):
	        return f'{self.doctor.pk}번 의사의 {self.patient.pk}번 환자'
	```
	📝 `through` : 인자에 전달한 값을 통해서 중개 모델이 작성되도록 한다.

	<br>

	예약 생성하기
	```python
	# 직접 생성
	reservation1 = Reservation(doctor=doctor1, patient=patient1, symptom='flu')
	
	# Patient 객체를 통해
	patient2.doctors.add(doctor1, through_defaults={'symptom': 'flu'})
	
	# Doctor 객체를 통해
	doctor1.patient_set.add(patient2, through_defaults={'symptom': 'flu'})
	```
4. 모델 간 관계가 복잡해 질 경우, manager 이름이 충돌할 수 있다. `related_name` 인자에 값을 지정해 해결한다.
	```python
	class Patient(models.Model):
	    doctors = models.ManyToManyField(Doctor, related_name='patients')
	    name = models.TextField()
	```
	`Doctor.patient_set` 대신 `Doctor.patients`라고 호출할 수 있다.

5. `symmetrical` (기본값 True)  
	모델이 자기 자신과 MTM 관계를 가질 수 있다. 예를 들어, 유저간 팔로우, 일촌과 같은 경우 User 모델이 자기 자신과 MTM 관계가 생긴다. 이때 관계가 단방향일지 양방향일지 symmetrical 인자에 False, True를 전달해 지정할 수 있다.
	```python
	class Person(models.Model):
		friends = models.ManyToManyField('self')
		# friends = models.ManyToManyField('self', symmetrical=False)
	```
	자신을 참조할 때 to 인자에 'self'를 전달한다. `symmetrical=True`로 지정하면 관계 1 → 2가 생성되면 2 → 1 또한 레코드에 작성된다.
	- `_set` 매니저를 추가하지 않음
	- "source 모델의 인스턴스가 target 모델의 인스턴스를 참조하면 자동으로 target 모델 인스턴스도 source 모델 인스턴스를 자동으로 참조하도록 함"
	
<br>

## 예시 - 좋아요
1. models.py  
	두 가지 방법 중 하나를 선택할 수 있다:
	1. User 모델 변경(accounts/models.py)
		```python
		class User(AbstractUser):
			like_articles = models.ManyToManyField('articles.Article', related_name='like_users')
			like_comments = models.ManyToManyField('articles.Comment', related_name='like_users')
			pass
		```
	2. Article과 Comment 모델 변경(articles/models.py)
		```python
		class Article(models.Model):
			user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
			like_users = models.ManyToManyField('articles.Article', related_name='like_articles')
			
			title = models.CharField(max_length=80)
			content = models.TextField(null=False)
		
		
		class Comment(models.Model):
			user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
			like_users = models.ManyToManyField('articles.Comment', related_name='like_comments')
			
			article = models.ForeignKey(Article, on_delete=models.CASCADE)
			content = models.TextField(null=False)
		```
		related_name과 필드 명을 어떻게 지정했는지 잘 구분하자. 두 경우 모두 같은 이름으로 related manager를 호출할 수 있다.
2. articles/urls.py
	```python
	urlpatterns = [
		    path('<int:article_pk>/likes', views.like_article, name='like_article'),
		    path('<int:article_pk>/comments/<int:comment_pk>/likes', views.like_comment, name='like_comment'),
	]
	```

3. articles/views.py
	```python
	@login_required
	def like_article(request, article_pk):
	    if Article.objects.filter(pk=article_pk).exists():
	        article = Article.objects.get(pk=article_pk)
	        if article.like_users.filter(pk=request.user.pk).exists():
	           article.like_users.remove(request.user)
	        else:
	            article.like_users.add(request.user)
	
	    return redirect('articles:detail', article_pk)
	
	
	@login_required
	def like_comment(request, article_pk, comment_pk):
	    if Article.objects.filter(pk=article_pk).exists() and Comment.objects.filter(pk=comment_pk).exists():
	        comment = Comment.objects.get(pk=comment_pk)
	        if comment.like_users.filter(pk=request.user.pk).exists():
	            comment.like_users.remove(request.user)
	        else:
	            comment.like_users.add(request.user)
	    
	    return redirect('articles:detail', article_pk)
	```

<br>

---
# 참고자료
- https://docs.djangoproject.com/en/3.2/ref/models/relations/#related-objects-reference
- 하이퍼그로스 교육자료 (18)

[^1]: