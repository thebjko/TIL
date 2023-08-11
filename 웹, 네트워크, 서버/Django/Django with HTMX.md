---
created_at : 2023-06-09, Fri
유효기록일 : 2023-06-09, Fri
topics : 
context : 
tags : django HTMX
related : 
---
# Django with HTMX
1. CDN, csrftoken
	```django
	...
	<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
	...
	
	  <script src="https://unpkg.com/htmx.org@1.9.2" integrity="sha384-L6OqL9pRWyyFU3+/bjdSri+iIphTN/bvYyM37tICVyOJkWZLpP2vGn6VUEXgzg6h" crossorigin="anonymous"></script>
	</body>
	...
	```
2. 사용법
	1. 각 태그 안에 사용할 수 있는 속성값을 지정한다
		- `hx-<method>` : `hx-get="<url>"`, `hx-post`, `hx-delete`, `hx-put`, `hx-post`
		- 값은 이동할 url이다.
		- `hx-target` : 타겟을 지정한다. id로 지정했다.
		- `hx-swap` : 어떻게 타겟을 변경할건지
		- `hx-confirm` : 확인 메세지를 alert창으로 띄운다.
	2. 폼 제출하기
		```django
		<div id="create-comment-on-{{ review.id }}" hx-target="#comment-list-{{ review.pk }}" hx-swap="outerHTML">
		  <form hx-post="{% url 'reviews:comment_create' review.pk %}">
		    {% with comment_form.content as content %}
		    <div class="form-group">
		      <textarea id="{{ content.id_for_label }}" class="form-control my-3" placeholder="{{ content.label }}" name="{{ content.name }}">test</textarea>
		    </div>
		    {% endwith %}
		    <div class="d-flex flex-row-reverse">
		      <button type="submit" class="button-small joinbutton">댓글 작성</button>
		    </div>
		  </form>
		</div>
		```
		`hx-post` 속성이 지정된 form 태그 안에 submit 타입 버튼을 만들어 놓으면, 클릭시 textarea의 textContent가 제출된다.

<br>



---
# 참고자료
- https://htmx.org/


[^1]: 
