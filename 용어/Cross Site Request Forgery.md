---
created : 2023-03-30, Thu
topics : Cross Site Request Forgery
alias : CSRF
context : django
related : 웹, 네트워크, 서버
---
# Cross Site Request Forgery
POST 요청을 중간에 가로채 위조(Forge)하는 해킹 공격.  Django는 `{% csrf_token %}`으로 세션과 토큰을 매치시켜 form이 유효한 세션에서 제출되었는지 검증한다.