---
created_at : 2023-04-19, Wed
유효기록일 : 2023-04-19, Wed
topics : 
context : django asynchronous 
tags : python/django javascript ajax
related : 
---
# Ajax로 팔로우(언팔로우)시 화면에 바로 반영하기
Django로 구현한 follow 뷰함수는 팔로우(언팔로우) 쿼리 수행 후 다시 프로필 페이지로 유저를 리다이렉트하는 방식으로 작동한다. 이런 경우 화면이 맨 위로 다시 올라가버리는 불편함이 발생한다. 자바스크립트와 Axios 클라이언트를 사용하면 화면을 이동하지 않고도 뷰함수의 리턴값을 받아 화면에 적용할 수 있다.

## 팔로우/언팔로우
0. 설치
	```html
	<!-- jsDelivr CDN -->
	<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

	<!-- unpkg CDN -->
	<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
	```
	CDN으로 HTML 문서에 입력한다.
	
현재 팔로우 버튼은 아래와 같다:
```django
<form action="{% url 'accounts:follow' person.pk %}" method="POST">
  {% csrf_token %}
  {% if request.user in person.followers.all %}
    <input type="submit" value="언팔로우">
  {% else %}
    <input type="submit" value="팔로우">
  {% endif %}
</form>
```
```python
@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect('accounts:profile', you.username)
```
버튼을 누르면 url을 타고 뷰함수를 실행해 새로 페이지를 로드한다.

form에서 submit 이벤트가 발생할 때 페이지를 다시 로드하지는 않되 데이터베이스에 반영하고, 반영된 값을 화면에 그리도록 코드를 수정할 것이다.

1. Form 요소 선택
	```js
	const form = document.getElementById("follow-form")

	form.addEventListener("submit", (event) => {
	  event.preventDefault()
	})
	```
	form 요소에 follow-form이라는 아이디를 주고 선택해 form 변수에 할당한다. form의 기본 행동은 submit이 발생하면 action 속성에 주어진 url로 이동한다. 이를 방지하기 위해 event의 `preventDefault()` 메서드를 실행한다.

2. Axios API 실행하기
	```js
		axios({
		  method: 'post',
		  url: `/accounts/${userId}/follow/`,
		  headers: {'X-CSRFToken': csrftoken},
		})
	```
	이벤트 리스너 안에서 axios 함수를 실행한다.
	1. method는 마찬가지로 'post'.
	2. userId를 받아서 accounts/urls.py를 통해 뷰함수가 실행할 수 있도록 url을 지정한다.
		```django
		<form id="follow-form" data-user-id="{{ person.pk }}">
          {% csrf_token %}
          {% if request.user in person.followers.all %}
            <input type="submit" value="언팔로우">
          {% else %}
            <input type="submit" value="팔로우">
          {% endif %}
        </form>
		```
		form 요소의 데이터셋 속성을 사용한다. 위와 같이 입력해 각 폼마다(여러개일 경우) `{{ person.pk }}`를 `data-user-id` 속성에 전달하면, 이벤트 리스너 안에서 `event.target.dataset.userId`와 같이 이용 가능하다. html은 대소문자를 구분하지 않기 때문에 user-id와 같이 입력하면 userId로 사용할 수 있다.
		```js
		const userId = event.target.dataset.userId
		```
	3. 메서드가 POST이기 때문에 csrf 토큰이 필요하다.
		```js
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
		```
		CSRFToken 또한 인풋 요소이다. name 속성이 위와 같으므로 쿼리셀렉터를 사용해 값을 가져온다.

3. axios 함수의 요청을 파이썬 뷰 함수로 처리해 JSONResponse 반환하기
	```python
	from django.http import JsonResponse
	
	@login_required
	def follow(request, user_pk):
	    User = get_user_model()
	    you = User.objects.get(pk=user_pk)
	    me = request.user
	
	    if you != me:
	        if me in you.followers.all():
	            you.followers.remove(me)
	            is_followed = False
	        else:
	            you.followers.add(me)
	            is_followed = True
	        context = {
	            'is_followed': is_followed,
	            'followings_count': you.followings.count(),
	            'followers_count': you.followers.count(),
	        }
	        return JsonResponse(context)   # axios의 리턴값 -> then의 response
	
	    return redirect('accounts:profile', you.username)
	```
	axios 함수는 결국 url로 요청을 보내 뷰함수를 호출하기 때문에 뷰 함수 또한 적절히 수정할 필요가 있다. 기본 골조는 같지만 리다이렉트로는 데이터를 전달할 수 없기 때문에 JsonResponse 객체를 사용한다. 전달되는 값을 살펴보자.
	1. `is_followed` : 현재 프로필 페이지에 나타나는 유저가 프로필 페이지를 보고 있는 유저에 의해 팔로우 되고 있는지
	2. `followings_count` : 몇 명을 팔로우하고 있는지
	3. `followers_count` : 몇 명이 이 유저를 팔로우하고 있는지
4. 반환된 값을 받아 화면에 표시하기
	```js
	.then((response) => {
	  const isFollowed = response.data.is_followed
	  const followBtn = document.querySelector('#follow-form > input[type=submit]')
	  if (isFollowed) {
	    // 팔로우o -> 언팔로우 버튼 뜨게
	    followBtn.value = '언팔로우'
	  } else {
	    // 팔로우x -> 팔로우 버튼 뜨게
	    followBtn.value = '팔로우'
	  }
	
	  const followingsCountTag = document.querySelector('#followings-count')   // span
	  const followersCountTag = document.querySelector('#followers-count')     // span
	
	  const followingsCountData = response.data.followings_count
	  const followersCountData = response.data.followers_count
	
	  // 선택한 span 태그의 내용을 팔로잉과 팔로워 수 데이터로 채워넣기
	  followingsCountTag.textContent = followingsCountData
	  followersCountTag.textContent = followersCountData
	})
	```
	axios 함수의 끝에서 호출한 then 메서드이다. 뷰함수에서 context로 전달한 데이터는 response.data로 접근할 수 있다. input 요소에 출력되는 값이 변경되어야 하므로 follow-form 아이디를 가진 form 요소의 *자식* 선택자로 해당 요소를 선택한다. 만약 팔로우되고 있으면 언팔로우 버튼이, 팔로우되고 있지 않으면 팔로우 버튼이 뜨도록 값을 할당한다.
	```django
	<div>
      팔로잉 : <span id="followings-count">{{ person.followings.all|length }}</span>
       / 팔로워 : <span id="followers-count">{{ person.followers.all|length }}</span>
    </div>
	```
	변경된 팔로워/팔로잉 수도 반영해야 한다. 그대로는 선택할 수 없으므로 span 요소로 감싸 followings-count, followers-count 아이디를 할당한다. textContent를 사용해 새로운 데이터를 채워넣는다. 이벤트가 발생했을때 실행되는 코드이다.

완성된 JavaScript 코드
```js
const form = document.getElementById("follow-form")
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
form.addEventListener("submit", (event) => {
  event.preventDefault()
  const userId = event.target.dataset.userId
  axios({
	method: 'post',
	url: `/accounts/${userId}/follow/`,
	// url: `/accounts/{{ person.pk }}/follow/` 안됨? -> 여러개일때 안되지
	headers: {'X-CSRFToken': csrftoken},
  }).then((response) => {
	// console.log(response.data.is_followed)
	// console.log(response['data'])
	const isFollowed = response.data.is_followed
	const followBtn = document.querySelector('#follow-form > input[type=submit]')
	if (isFollowed) {
	  // 팔로우o -> 언팔로우 버튼 뜨게
	  followBtn.value = '언팔로우'
	} else {
	  // 팔로우x -> 팔로우 버튼 뜨게
	  followBtn.value = '팔로우'
	}

	const followingsCountTag = document.querySelector('#followings-count')   // span
	const followersCountTag = document.querySelector('#followers-count')     // span

	const followingsCountData = response.data.followings_count
	const followersCountData = response.data.followers_count

	// 선택한 span 태그의 내용을 팔로잉과 팔로워 수 데이터로 채워넣기
	followingsCountTag.textContent = followingsCountData
	followersCountTag.textContent = followersCountData
  })
})
```

<br>

## 좋아요
좋아요는 모든 게시물/댓글에, 경우에 따라서는 한 페이지에 구현해야하므로 복잡할 수 있다. `forEach` 메서드와 모든 해당하는 요소를 선택하는 `querySelectorAll`을 사용해 구현한다.

```django
<form class="like-forms" data-article-id="{{ article.pk }}">
  {% csrf_token %}
  {% if user in article.like_users.all %}
    <input type="sumbmit" value="좋아요 취소" id="like-{{ article.pk }}">
  {% else %}
    <input type="submit" value="좋아요" id="like-{{ article.pk }}">
  {% endif %}
</form>
```

```python
from django.http import JsonResponse

@login_required
def likes(request, article_pk):
    article = Article.objects.get(pk=article_pk)

	if request.user in article.like_users.all():
	    article.like_users.remove(request.user)
	    is_liked = False
	else:
		article.like_users.add(request.user)
		is_liked = True
	context = {
		'is_liked': is_liked,
	}
	return JsonResponse(context)
```

```js
const forms = document.querySelectorAll('.like-forms')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value   // 자식선택?

forms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()
    const articleId = event.target.dataset.articleId
    axios({
      method: 'post',
      url: `/articles/${articleId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    }).then((response) => {
      const isLiked = response.data.is_liked
      const likeBtn = document.querySelector(`#like-${articleId}`)
      if (isLiked) {
        likeBtn.value = '좋아요 취소'
      } else {
        likeBtn.value = '좋아요'
      }
    }).catch((error) => {   // 에러 메세지 출력
      console.log(error.response)
    })
  })
})
```
📈 CSRF Token들은 한 페이지에서 모두 같은 값을 가지고 있다.

<br>

---
# 참고자료
- 하이퍼그로스 교육자료

[^1]: