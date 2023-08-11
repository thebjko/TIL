---
created_at : 2023-08-11, Fri
유효기록일 : 2023-08-11, Fri
topics : 
context : FastAPI
tags : postgresql pgadmin4
related : 
---
# 맥에서 PostgreSQL 및 PgAdmin4 사용해 로컬 DB 서버 사용하기

아래의 두 커맨드로 postgresql과 pgadmin4를 설치
```
brew install postresql
brew install --cask pgadmin4
```

서버 구동
```
brew services start postgresql@14
```

PgAdmin4 실행 후 Servers를 오른쪽 클릭 후 Register → Server 또는 Add new server 클릭
![[pgAdmin4 메인화면.png]]

Name 입력
![[pgAdmin4 - General.png]]

Connection 탭에서 Host name 입력
![[pgAdmin4 - Connection.png]]

계정 확인
![[postgres 계정 확인.png]]
계정이 없을 경우 생성한다.[^1]

```sql
CREATE ROLE {사용자명} WITH LOGIN PASSWORD '{비밀번호}';
ALTER ROLE {사용자명} CREATEDB;   -- DB 생성 권한 부여
```

Connection 탭에서 Username 입력 후 SAVE
![[pgAdmin4 - Username.png]]

잘 생성되었다.
![[pgAdmin4 - 서버 만들기 완료화면.png]]

<br>

---
# 참고자료
- [psql: FATAL: role "postgres" does not exist](https://stackoverflow.com/questions/15301826/psql-fatal-role-postgres-does-not-exist)


[^1]: [Create Role](https://kth990303.tistory.com/414)
