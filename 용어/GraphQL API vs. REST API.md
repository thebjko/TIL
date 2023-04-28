---
created_at : 2023-04-24, Mon
유효기록일 : 2023-04-24, Mon
topics : 
context : 
tags : rest_api graphql_api
related : 
---
# REST API
📝 REST(Representational State Transfer) 표준을 따르는 API. REST 요청은 endpoint, HTTP method, Header, Body로 이루어져있다.
- `GET` reads a representation of a specified source.
- `POST` creates a new specified source.
- `PUT` updates/replaces every resource in a collection.
- `PATCH` modifies a source.
- `DELETE` deletes a source.

---

- 다양한 Endpoint
	- 각 Endpoint마다 DB SQL 쿼리가 달라진다.
- Resource가 핵심 : 각 리소스는 URL endpoint로 정의되고, 특정 HTTP Method로 요청해 데이터를 가져온다. 
- Resource에 대한 형태 정의와 데이터 요청 방법이 연결되어 있다
- Resource의 크기와 형태를 서버에서 결정
- URI가 Resource를 나타내고 Method가 작업의 유형을 나타냄
- 여러 Resource에 접근하고자 할 때 여러 번의 요청이 필요
- 각 요청은 해당 엔드포인트에 정의된 핸들링 함수를 호출하여 작업을 처리

![일반 HTTP API 적용 스택 vs. GraphQL 적용 스택](http://tech.kakao.com/files/graphql-stack.png)

<br>

# GraphQL API
- 하나의 Endpoint
	- Schema의 타입마다 DB SQL 쿼리가 달라진다.
- Resource에 대한 형태 정의와 데이터 요청이 완전히 분리되어 있다
- Resource에 대한 정보만 정의하고, 필요한 크기와 형태는 client단에서 요청 시 결정
- GraphQL Schema가 Resource를 나타내고 Query, Mutation 타입이 작업의 유형을 나타냄
- 한번의 요청에서 여러 Resource에 접근할 수 있다
- 요청 받은 각 필드에 대한 resolver를 호출하여 작업을 처리

![HTTP vs gql](http://tech.kakao.com/files/graphql-mobile-api.png)
위 그림처럼 gql API를 사용하면 여러번 네트워크 호출을 할 필요 없이, 한 번의 네트워크 호출로 처리할 수 있다.

<br>

## 예시
요청: 
```graphql
{
  hero {
    name
  }
}
```
응답:
```json
{
  "data": {
    "hero": {
      "name": "R2-D2"
    }
  }
}
```

<br>

# HOW TO CONVERT

<br>

# HOW TO USE GRAPHQL WITH DJANGO

<br>

---
# 참고자료
- https://hygraph.com/blog/graphql-vs-rest-apis
- https://hwasurr.io/api/rest-graphql-differences/
- https://tech.kakao.com/2019/08/01/graphql-basic/
- https://www.howtographql.com/basics/1-graphql-is-the-better-rest/
- https://blog.logrocket.com/graphql-vs-rest-api-why-you-shouldnt-use-graphql/
- https://docs.graphene-python.org/en/latest/quickstart/#introduction
- https://www.codecademy.com/article/smyja/how-to-use-graphql-with-django
- https://cholol.tistory.com/496

[^1]: