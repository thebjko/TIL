---
created_at : 2023-05-13, Sat
유효기록일 : 2023-05-13, Sat
topics : 
context : 
tags : django sqlectron mysql localhost
related : 
---
# MySQL Localhost to Sqlectron or Django
내컴퓨터에서 실행한 MySQL서버로 연결하기

1. mysql 서버 실행 
```zsh
> mysql.server start
```
2. mysql 설치 시 입력한 root 유저 비밀번호를 사용해 로그인
```zsh
> mysql -u root -p
```
위 명령 실행 후 비밀번호 입력 프롬프트가 뜨면 입력하고 엔터

3. mysql 접속
```zsh
> mysql
```
4. 사용할 데이터베이스 생성
```zsh
mysql> CREATE DATABASE mydb;
Query OK, 1 row affected (0.00 sec)
```
5. Sqlectron 실행 후 Add 클릭
6. 필요한 정보 입력
	- Name : 다른 연결들과 구분할 이름
	- Database Type : `MySQL`
	- Server Address : `localhost`
	- User : `root`
	- Password : 유저 비밀번호
	- Initial Database/Keyspace : 아까 생성한 `mydb` 입력
7. Test 후 성공시 Save 클릭
8. Connect 클릭하여 접속

<br>

0. Django와 연동하기
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
마이그레이션 실행 후 확인하기
```zsh
python manage.py migrate
```
```zsh
mysql> SHOW TABLES FROM mydb;
+--------------------------------+
| Tables_in_mydb                 |
+--------------------------------+
| accounts_user                  |
| accounts_user_followers        |
| accounts_user_groups           |
| accounts_user_user_permissions |
| auth_group                     |
| auth_group_permissions         |
| auth_permission                |
| boss_address                   |
| boss_category                  |
| boss_indexcarouselimage        |
| boss_order                     |
| boss_order_items_to_ship       |
| boss_product                   |
| boss_product_like_users        |
| boss_review                    |
| boss_review_like_users         |
| boss_reviewimage               |
| boss_subcategory               |
| django_admin_log               |
| django_content_type            |
| django_migrations              |
| django_session                 |
+--------------------------------+
22 rows in set (0.00 sec)
```

<br>

---
# 참고자료
- [Install MySQL community server](https://www.prisma.io/dataguide/mysql/setting-up-a-local-mysql-database#setting-up-mysql-on-macos)
- ChatGPT


[^1]: 
