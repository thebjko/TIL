---
created_at : 2023-04-18, Tue
유효기록일 : 2023-04-18, Tue
topics : 
context : 11_django_many_to_many
tags : python/django/models/relations database
related : 
---
# 자기 자신과 Many To Many Relationship 
## User & User - Follow 기능
1. accounts/models.py
	```python
	class User(AbstractUser):
		# to 인자에 문자열 'self'를 전달
	    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
	```
	User 모델이 User 모델과 다대다 관계를 갖는다. 한 유저가 여럿 팔로우 할 수 있고, 또 여럿에게 팔로우를 받을 수 있다. Migrate 하면 from\_user\_id, to\_user\_id 컬럼을 갖는 accounts\_user\_followings 테이블이 생긴다. **from\_user가 to\_user를 팔로우하는 관계**를 표현하는 중개 테이블이다.  
	한 user가 팔로우 하고 있는 사람들을 조회하려면 `user.followings.all()`, user를 팔로우 하고 있는 사람들을 조회하려면 `user.followers.all()`을 실행하면 된다.

	만약 필드명을 followers로 하고 related\_name을 'followings'로 하면, accounts\_user\_followings 테이블이 생기고, 여전히 from\_user\_id, to\_user\_id 컬럼이 생긴다. 다만 컬럼의 의미를 약간 다르게 해석해야 한다. from\_user\_id가 팔로우 받는다는 의미이다(이 유저의 팔로잉). 

	1 대 1 관계에서 ForeignKey를 사용하는 모델이 참조하는 모델(ForeignKey 필드의 to 인자에 넘겨준 모델)이 ForeignKey를 사용하는 모델을 역참조할 때 related manager를 사용했다. 다대다 관계에서는 양방향에서 사용할 수 있는데, 먼저 두 개의 모델이 다대다 관계일 때를 생각해보자:
	```python
	class Topping(models.Model):
	    # ...
	    pass
	
	class Pizza(models.Model):
	    toppings = models.ManyToManyField(Topping)	
	```
	이 경우 `Pizza.toppings`와 `Toppings.pizza_set`로 related manager를 호출했다. Topping은 Pizza를 역참조하고, Pizza가 Topping을 참조하고 있다. 다대다 관계에서는 참조할 때 필드명으로, 역참조할 때 related_name으로 related manager를 호출한다.

	따라서 자기 자신을 참조하는 다대다 관계에서도 마찬가지인데, 사실 아래에서 볼 수 있듯 뷰함수에서 상대방의 followers에 나(me)를 추가/삭제하기 때문에 필드명을 followers, related_name을 followings로 지정해도 별다른 차이가 없다. 심지어 필드명을 followings로 하고 `you.followings.remove(me)`를 실행해도 된다. 다만 의미가 반대이므로 사람이 이해하기 힘들 뿐이다. 아래의 예를 참고:

	accounts/models.py
	```python
	class User(AbstractUser):
	    followers = models.ManyToManyField('self', related_name='followings', symmetrical=False)
	```
	accounts/views.py
	```python
	@login_required
	def follow(request, user_pk):
	    User = get_user_model()
	    you = User.objects.get(pk=user_pk)
	    me = request.user
	    if you == me:
	        return redirect('accounts:profile', me.username)
	    
	    if me in you.followers.all():
	        you.followers.remove(me)
	    else:
	        you.followers.add(me)
	
	    return redirect('accounts:profile', you.username)
	```
	id가 3인 유저가 4인 유저 팔로우시 from\_user\_id에 4, to\_user\_id에 3이 기록된다.

📝 결론 : 자기 자신을 참조하는 다대다 관계에서는 필드명과 related manager 이름이 기능에는 크게 중요하지 않지만 의미를 명확히 하기 위해 이름을 잘 작성하자.

2. accounts/views.py
	```python
	@login_required
	def follow(request, user_pk):
	    User = get_user_model()
	    you = User.objects.get(pk=user_pk)
	    me = request.user
	    if you == me:
	        return redirect('accounts:profile', me.username)
	
	    if me in you.followers.all():
	        you.followers.remove(me)
	        # me.followings.remove(you)
	    else:
	        you.followers.add(me)
	        # me.followings.add(you)
	    
	    return redirect('accounts:profile', you.username)
	```
	프로필을 조회하는 기능은 계정과 관련되어있기 때문에 accounts 어플리케이션에서 진행한다. follow 함수가 호출되었을 때 이미 팔로우가 되어있는 상태라면 팔로우 취소, 그렇지 않다면 팔로우해야한다. `request.user`는 현재 로그인 한 유저 정보를 갖고 있고, 팔로우 하는 대상은 user\_pk로 User 모델에 쿼리를 넣어 가져온다.
	```python
		User = get_user_model()
	    you = User.objects.get(pk=user_pk)
	    me = request.user
	```
	여기서 변수명은 이해하기 쉽게 you(팔로우 대상)와 me(로그인한 유저)로 한다. 자기 자신은 팔로우할 수 없도록 한다.
	```python
		if you == me:
	        return redirect('accounts:profile', me.username)
	```
	User 모델에서 역참조하기 위한 related manager 이름을 'followers'로 했다. 따라서 팔로우 할 대상 you 객체에서 `you.followers.all()`은 you를 팔로우하는 모든 user를 조회한다. 아래와 같이 `you.followers`로 related manager를 호출해 삭제, 추가를 수행하던, `me.followings`로 정참조해 같은 작업을 하던 결과는 같다.
	```python
		 if me in you.followers.all():
		    # if person.followers.filter(pk=request.user.pk).exists():   pk??
	        you.followers.remove(me)
	        # me.followings.remove(you)
	    else:
	        you.followers.add(me)
	        # me.followings.add(you)
	```
	여기서는 프로필 페이지로 리다이렉트 하고 있지만, 다른 곳에서 팔로우 버튼을 구현할 경우 [[reverse(), resolve()]] 함수를 적절히 사용해 왔던 곳으로 되돌아 갈 수도 있을 것 같다.
3. accounts/profile.html
	```django
	<div>
	  팔로잉 : {{ person.followings.all.count }} / 팔로워 : {{ person.followers.all.count }}
	</div>
	{% if user != person %}
	<div>
	  <form action="{% url 'accounts:follow' person.pk %}" method="post">
	    {% csrf_token %}
	    {% if user in person.followers.all %}
	    <input type="submit" value="팔로우 취소">
	    {% else %}
	    <input type="submit" value="팔로우">
	    {% endif %}
	  </form>
	</div>
	```

<br>

---
# 참고자료
- 하이퍼그로스 교육자료 : "19\_django\_many\_to\_many\_relationship"
- https://docs.djangoproject.com/en/3.2/ref/models/relations/

[^1]: