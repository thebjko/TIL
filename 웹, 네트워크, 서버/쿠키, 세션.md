---
created : 2023-04-04, Tue
유효 기록일 : 2023-04-04, Tue
topics : 쿠키, 세션
context : django Authentication
tags : cookie, session, http_protocol
related : django
---
# HTTP 프로토콜의 특징
1. Connectionless (비연결 지향)
	- 클라이언트가 서버에 요청 했을 때 응답 후 연결을 끊는다. 
2. Stateless (무상태)
	- 커넥션을 끊는 순간 클라이언트와 서버 간 통신이 끝나고 상태는 유지되지 않는다.

정보가 유지되지 않으면, 로그인 상태나, 장바구니에 담긴 물건들처럼 지속적으로 유지되어야 하는 경우 쿠키와 세션을 통해 상태 정보를 저장한다.

<br><br>
# 쿠키
> 서버에서 발급해 클라이언트 사이드(브라우저)에 저장되는 텍스트 조각. 

<br>

## 특징
1. 이름, 값, 만료일, 경로 정보로 구성
2. 클라이언트에 총 300개의 쿠키를 저장할 수 있음
3. 하나의 도메인 당 20개의 쿠키를 가질 수 있음
4. 하나의 쿠키는 약 4KB 까지 저장 가능

<br>

## 예시
1. 아이디와 비밀번호 저장
2. 장바구니
3. 팝업창 -> 오늘 이 창을 다시 보지 않기

<br><br>
# 세션
> 로그인 여부 등 사용자와 서버의 관계가 기억되어 보존되고 있는 상태.[^1] 일정 시간 동안 같은 사용자(브라우저)로부터 들어오는 일련의 요구를 하나의 상태로 보고, 그 상태를 유지시키는 기술.[^2]

<br>

## 특징
1. 웹 서버에 웹 컨테이너의 상태를 유지하기 위한 정보를 저장(= 세션 쿠키)
2. 브라우저를 닫거나, 서버에서 세션을 삭제했을 때만 삭제가 되므로, 쿠키보다 비교적 보안이 좋다.
3. 저장 데이터에 제한이 없다. (서버 용량이 허용하는 한에서)
4. 각 클라이언트에 고유 Session ID를 부여한다.

<br>

## 예시
1. 화면 이동시에도 로그인 유지


<br><br>
# 토큰
> 메모리를 많이 차지하는 세션 방식 대신 토큰을 발급해 쿠키에 저장하는 방식으로 로그인을 유지하기도 한다.

<br>

## 단점
- 서버에서 사용자를 강제로 로그인시킬 수 없다.
- 이는 토큰이 탈취당했을 때 보안상 문제가 된다.
- 만료기간을 짧게 하는 방식으로 피해를 줄인다.

<br>

## JWT
> JSON Web Token : JSON의 형태로 정보를 안전하게 주고받기 위한 토큰.[^3] 주로 인증과 전달된 정보의 신뢰성을 보증하기 위해 사용된다.[^4]

- [[HMAC]], [[RSA]], [[ECDSA]]로 전자 서명이 가능
- [[Single Sign On]]이 JWT를 사용한다
- 주고받는 정보의 내용이 제 3자에 의해 중간에 조작되지 않았음을 확인할 수 있다

<br>

### JWT의 구조
> `xxxxx.yyyyy.zzzzz` : Header, Payload, Signature

<br>

#### Header
- 토큰 타입("JWT")
- 서명 알고리즘 (ex. HMAC SHA256 or RSA)

<br>

#### Payload
> 클레임

클레임의 세가지 종류
- Registered claims: 사전에 정의된 클레임 (ex. is, exp, sub, aud 등)
- Public claims: 필요에 따라 IANA JSON Web Token Registry에 등록하는 클레임을 정의할 수 있다
- Private claims: 당사자간 약속해 사용하는 클레임

<br>

#### Signature
중간에 변경되지 않았음을 증명


<br><br>
# 더 공부해 볼 것
- [Django에서 세션 사용하기](https://docs.djangoproject.com/en/3.2/topics/http/sessions/)
- [Django REST Framework with JWT](https://www.qu3vipon.com/django-jwt)
- [Django REST Framework with JWT](https://dev-yakuza.posstree.com/en/django/jwt/)
- Django REST Framework with JWT[^4]



<br><br>
# 참고자료
[^1]: https://hongong.hanbit.co.kr/%EC%99%84%EB%B2%BD-%EC%A0%95%EB%A6%AC-%EC%BF%A0%ED%82%A4-%EC%84%B8%EC%85%98-%ED%86%A0%ED%81%B0-%EC%BA%90%EC%8B%9C-%EA%B7%B8%EB%A6%AC%EA%B3%A0-cdn/
[^2]: https://dev-coco.tistory.com/61
[^3]: https://jwt.io/introduction
[^4]: https://www.freecodecamp.org/news/how-to-use-jwt-and-django-rest-framework-to-get-tokens/
[^5]: https://github.com/lemon-lime-honey/TIL/blob/main/django/cookie_session.md