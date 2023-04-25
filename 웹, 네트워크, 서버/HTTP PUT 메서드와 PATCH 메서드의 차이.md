---
created_at : 2023-04-25, Tue
유효기록일 : 2023-04-25, Tue
topics : 
context : rest_api 
tags : rest_api http
related : 
---
# PUT
리소스의 모든 것을 업데이트한다.

<br>

# PATCH
리소스의 일부를 업데이트한다

<br>

# 예시

이름, 나이, 성별이라는 필드를 가진 레코드(리소스)가 있다고 하자.
1. PUT으로 `{name: '킬복순'}`이라고 보내면 나이와 성별 필드에 있던 데이터가 사라진다.
2. 반면, PATCH로 같은 메서드를 보내면 다른 필드는 유지된 채로 이름만 업데이트된다.

<br>

---
# 참고자료
- https://programmer93.tistory.com/39

[^1]: