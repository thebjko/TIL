---
created_at : 2023-04-25, Tue
유효기록일 : 2023-04-26, Wed
topics : Django에서 QueryParameter 사용하기
context : 
tags : 
related : 
---
# Django에서 QueryParameter 사용하기
## URL에서 QueryParameter 사용하기  
QueryParaemeter가 다음과 같다고 하자:
```
domain/search/?q=haha
```
뷰 함수 내에서 아래와 같이 사용할 수 있다.
```python
request.GET.get('q', '')   # list
```

<br>

## QueryParameter로 요청하기
1. POSTMAN : Params 탭에 키 값 쌍을 넣어서 요청한다.
2. requests 라이브러리를 사용한다.
	```python
	import requests
	
	requests.get('q', params={'query': 'something'})
	```


---
# 참고자료
- https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
- https://youtu.be/c708Nf0cHrs

[^1]: