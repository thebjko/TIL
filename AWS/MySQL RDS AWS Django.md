---
created_at : 2023-05-10, Wed
유효기록일 : 2023-05-11, Thu
topics : 
context : Baemin(사장님의 냉장고 프로젝트, 냉django를 채워조)
tags : mysql django aws rds
related : 
---
# Django - RDS MySQL 셋업
0. mysqlclient 설치 - Python interface to MySQL
```
pipenv install mysqlclient
```
1. 여러 데이터베이스를 사용하기 위해 다음과 같은 코드를 세팅 파일에 추가한다. dev.py와 prod.py를 구분해 사용하고 있으므로 일단 dev.py를 수정한다. 'users'라는 이름으로 MySQL DB를 사용할 것이다.
```python
if 'RDS_HOSTNAME' in os.environ:
    DATABASES['users'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('RDS_DB_NAME'),
        'USER': os.getenv('RDS_USERNAME'),
        'PASSWORD': os.getenv('RDS_PASSWORD'),
        'HOST': os.getenv('RDS_HOSTNAME'),
        'PORT': os.getenv('RDS_PORT'),
    }
```

2. migrate를 `users`로 한다
```
python manage.py migrate --database=users
```

> fixture 사용도 마찬가지로 `python manage.py loaddata myFixtures.json --database=users` 사용

3. 모델 매니저를 사용할 경우 `using`메서드를 사용한다
```python
Post.objects.using('users').all()
```

<br>

# EC2에 올릴 경우 민감한 정보 처리하기
`.env` 파일로 인스턴스 내 저장하는 것은 보안 측면에서 좋지 않다고 한다. AWS는 Secrets Manager라는 비밀번호 저장소를 제공한다. 

1. boto3
```python
import boto3
import json

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='{지정한 secret 이름}')   # returns JSON

```

Secrets Manager에서 시크릿을 등록할 때는 더 상세한 코드를 제공한다.
```python
import boto3, json
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name) -> dict:
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    # Your code goes here.
    return json.loads(secret)
```
약간 수정해 `secret_name`과 `region_name`을 인자로 받고 dictionary를 반환함을 명시했다. `get_secret_value_response`는 JSON을 리턴하는데 이를 `json.loads`를 사용해 파이썬 딕셔너리로 변환 후 반환한다.

> 아직 이해가 안간다. EC2에 Secrets Manager로 액세스 할 권한이 있으면 EC2에 들어온 아무나 Secrets Manager에 저장된 민감한 정보를 fetch할 수 있다는 말 아닌가?
> 
> 1. 매번 `.env` 파일에 저장하면 관리가 어려울 수 있다.
> 2. Automatic Rotation 기능이 있다.

2. 완성된 코드
dev.py
```python
# mysql database
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
if 'RDS_HOSTNAME' in os.environ:
    secrets = get_secret(
        secret_name=os.getenv('SECRET_NAME'),
        region_name=os.getenv('REGION_NAME'),
    )
    '''
    Model Manager를 'users' DB를 사용하도록 일일이 커스텀 할 수 없어서
    RDS 관련 정보가 환경변수에 있는 경우 MySQL을 디폴트 DB로 사용하도록 수정
    '''
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('RDS_DB_NAME'),
        'USER': secrets.get('username'),
        'PASSWORD': secrets.get('password'),
        'HOST': os.getenv('RDS_HOSTNAME'),
        'PORT': os.getenv('RDS_PORT'),
    }
    # print(DATABASES['default']['PASSWORD'])   # 출력이 되긴 한다.
```

prod.py는 `.env` 파일이 있다는 가정 하에 if문을 제거한 것 빼고는 위와 동일하다. base.py에 `get_secret` 함수를 추가해 dev.py와 prod.py에서 사용할 수 있게 했다.

<br>

# MySQL(RDS) 연결
## CLI
```
mysql --host={RDS_HOSTNAME} --user={RDS_USERNAME} --password
```
password 뒤로 비워두면 password를 입력하라는 프롬프트로 이어진다. 방식이 `--password={RDS_PASSWORD}`로 직접 입력하는 것보다 안전하다고 한다.

어떤 DB를 사용할 것인지 입력한다
```sql
mysql> USE BossmarketDB
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```
`RDS_DB_NAME`에 해당하는 값을 전달한다.

`loaddata` 후 정보가 잘 들어갔는지 확인하기 위해 `boss_category` 테이블 조회
```sql
mysql> SELECT * FROM boss_category;
+----+------------------+
| id | name             |
+----+------------------+
| 15 | 가공식품         |
| 16 | 농수축산물       |
| 17 | 배달용품         |
| 18 | 주방용품         |
| 19 | 렌탈/서비스      |
| 20 | 테마관           |
+----+------------------+
6 rows in set (0.01 sec)
```


테이블 목록 구하기
```sql
mysql> SHOW tables;
+--------------------------------+
| Tables_in_BossmarketDB         |
+--------------------------------+
| accounts_user                  |
| accounts_user_followers        |
| accounts_user_groups           |
| accounts_user_user_permissions |
| auth_group                     |
| auth_group_permissions         |
| auth_permission                |
| boss_category                  |
| boss_product                   |
| boss_product_like_users        |
| boss_review                    |
| boss_reviewimage               |
| boss_subcategory               |
| django_admin_log               |
| django_content_type            |
| django_migrations              |
| django_session                 |
+--------------------------------+
```

테이블 삭제 [^1]

```sql
DROP DATABASE [IF EXISTS] database_name;
```
<br>

## SQLECTRON
> A simple and lightweight SQL client with cross database and platform support. [깃허브 저장소 링크](https://github.com/sqlectron/sqlectron-gui)

~~MySQL워크벤치여 안녕~~

1. 설치
```
brew install --cask sqlectron
```

2. Add 선택
![[Add 선택.png]]
3. 각 정보를 입력한다
![[정보 입력.png]]
- Name : Sqlectron에 등록된 다른 서버와 구분하기 위해 입력하는 값
- Database Type : MySQL
- Server Address : `RDS_HOSTNAME`에 해당하는 값
- User : `secrets.get('username')`에 해당하는 값
- Password : `secrets.get('password')`에 해당하는 값
- Initial Database/Keyspace : `RDS_DB_NAME`에 해당하는 값

4. 결과
![[결과 - Connect 클릭.png]]
Connect를 클릭하면 쿼리를 입력할 수 있는 창과, 테이블 목록을 볼 수 있는 왼쪽 사이드바를 볼 수 있다.
![[MySQL서버(RDS)와 연결된 화면.png]]

---
# 참고자료
1. [Django - How to Use Multiple DB](https://docs.djangoproject.com/en/4.2/topics/db/multi-db/)
2. [AWS Documentation on How to Set up DB in Django](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html)
3. [Django Database Setting](https://docs.djangoproject.com/en/4.2/ref/settings/#databases)
4. [Boto3 Secrets Manager Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html)
5. [Python - How to access DB credentials from AWS Secrets Manager? | AWS Secrets Manager Tutorial](https://youtu.be/CxEmaWP7fGE)
6. [Secrets Manager Documentation on `get_secret_value`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html)
7. [Amazon RDS Documentation on Using DB with Secrets Manager](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html)
8. [HOSTNAME 등, DB 정보 찾기 - AWS Doc](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html)
9. [CLI로 MySQL DB 연결하기](https://dev.mysql.com/doc/refman/8.0/en/connecting.html)
10. [AWS Secrets Manager: Amazon RDS integration for master user password management](https://youtu.be/tAXYA9QAR2o)
11. [Move hardcoded database credentials to AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/hardcoded-db-creds.html)


[^1]: https://www.mysqltutorial.org/mysql-drop-database/