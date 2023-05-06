---
created_at : 2023-05-02, Tue
유효기록일 : 2023-05-05, Fri
topics : 
context : TeamProject1
tags : aws/s3 aws/ec2 deploy python/django/deploy staticfiles mediafiles
related : 
---
# Django 어플리케이션과 AWS S3 연동하기
[[Django 어플리케이션 AWS EC2 인스턴스로 배포하기|Django 어플리케이션을 AWS EC2 인스턴스에 배포]]했는데, 어플리케이션이 정적 파일들을 사용하지 못하고 있다. 조사해보니 배포시에는 다른 디렉토리를 사용한다고 한다. (실제 사용 환경을 가정하면) 얼마나 많은 용량이 필요할지 몰라 S3를 사용하기로 한다. Media 파일도 같이 저장해서 사용할 수 있다는 장점도 있다.

<br>

## AWS
### EC2 인스턴스에 AmazonS3FullAccess 권한 부여하기
EC2 인스턴스를 통해 CRUD가 가능해야한다. EC2에 직접 설정해주는 방법도 있지만, AmazonS3FullAccess 권한을 가진 IAM 역할을 만들고 EC2에 그 역할을 부여하는 방법으로 진행한다. EC2가 삭제되어도 IAM 역할은 유지되기 때문에 이 방법이 개발할 때 더 실용적인것 같다.

Amazon IAM으로 이동 및 왼쪽 탭에 있는 '역할' 클릭
![[IAM 사이드바.png]]

역할 만들기
![[IAM 역할 만들기.png]]

신뢰할 수 있는 엔터티 유형 → AWS 서비스, 사용 사례 → EC2 선택 후 다음
![[IAM 신뢰할 수 있는 엔터티.png]]

S3 검색 후 AmazonS3FullAccess 체크 및 다음
![[IAM 권한 정책 선택.png]]

이름을 지정하고 역할을 생성한다. 다시 역할 섹션으로 돌아와보면 방금 만든 역할이 생성되어있다. EC2로 이동한다.

IAM 역할을 부여할 인스턴스 선택 → 작업 → 보안 → IAM 역할 수정
![[IAM 역할 수정.png]]

해당 IAM 역할 선택 후 IAM 역할 업데이트 클릭
![[IAM 역할 업데이트.png]]

역할이 부여되었다.

<br>

### Create S3 bucket
Amazon S3로 이동 → 버킷 만들기 클릭
![[S3 버킷 만들기.png]]

버킷 이름은 고유해야 한다. 어떤 사람도 같은 이름을 가진 버킷이 없어야 한다. AWS 리전은 EC2 인스턴스가 있는 리전과 같게 선택한다. 
![[S3 버킷 이름 및 리전.png]]

모든 퍼블릭 액세스 차단을 해제(체크해제) 한 채로 버킷 만들기를 클릭한다.
![[퍼블릭 액세스.png]]

### 버킷 정책 설정

권한 탭 → 버킷 정책 → 편집 선택
![[S3 권한 설정 1.png]]
![[S3 버킷 정책.png]]

버킷 ARN을 복사하고 정책 생성기 클릭.
![[S3 버킷 정책 편집.png]]

Select Type of Policy → S3 Bucket Policy
![[S3 버킷 정책 편집 2.png]]

진행에 앞서 버킷 정책에 대해 생각해보자.[^5] IAM 유저/역할이 S3에 접근할 때, 아래의 정책들이 적용된다:
- IAM 정책
- 그룹 정책
- 버킷 정책

버킷 정책은 아래와 같이 동작한다:

1. 명시적인 거부가 있다면 적용된다. 그렇지 않으면
2. 명시적인 허용이 있다면 적용된다. 그렇지 않으면
3. 모든 접근이 거부된다.

즉 아무 정책도 없으면 모든 접근이 거부된다. 명시적인 거부와 허용이 같은 Principal, Action에 있다면 거부가 적용된다. 

현재 이 프로젝트는

1. 모든 사용자가 웹사이트에서 스태틱 파일을 사용할 수 있게 해야 한다. EC2에 있는 Django 어플리케이션을 이용하지만 GetObject는 Client 레벨에서 발생하는 것 같다. 모든 Principal(`'*'`)에 대해 GetObject를 허용한다.
2. 내 Django 어플리케이션을 통해서만 Create, Update, Delete가 가능해야 한다. 좀 더 정확히 말하면 '내 어플리케이션이 배포된 EC2 인스턴스를 통해서만' 가능하게 할 것이다. 어플리케이션이 배포된 EC2 인스턴스의 IAM 역할에 AmazonS3FullAccess를 부여해 이를 이룰 것이므로 버킷 정책을 더할 필요가 없다.

#### 모든 사용자에 대해 Read 권한 부여하기
- Effect : Allow
- Principal : `*`
- Actions : GetObject 체크
- Amazon Resource Name (ARN) : 아까 복사해둔 ARN을 붙여넣고 **뒤에 `/*`을 붙여**서 해당 서비스에 있는 모든 오브젝트를 가리킴을 명시한다.

Add Statement 클릭

![[Add Statements.png]]
![[Statements.png]]

Generate Policy 클릭 후 뜨는 JSON 문서를 복사한다. 
![[Policy JSON Document.png]]

버킷 정책 편집창으로 돌아와 기존 내용 삭제 후 붙여넣고 저장.
![[GetObject to All.png]]

```json
{
	"Version": "2012-10-17",
	"Id": "Policy1683291350206",
	"Statement": [
		{
			"Sid": "Stmt1683291324706",
			"Effect": "Allow",
			"Principal": "*",
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::my-mangoplateproject-bucket-2023-goldang/*"
		}
	]
}
```

<br>

## Django
### 필요 패키지 설치
django-storages와 boto3를 설치한다. django-storage는 django가 커스텀 백엔드 저장소를 사용할 수 있게 해주는 패키지이고, boto3은 파이썬으로 Amazon SDK를 제공해주는 패키지이다.
```
# django-storages
pip install django-storages
pipenv install django-storages

# Amazon SDK for python development
pip install boto3
pipenv install boot3
```

settings.py
```python
INSTALLED_APPS += ['storages',]   # django-storages
```

### AWS S3 관련해 django-storages 변수들에 값을 할당한다.
이 부분은 Django 4.2부터는 달라지니 [django-storages 공식 문서를 참고](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings)하라.

settings.py
```python
# AWS_ACCESS_KEY_ID = ""
# AWS_SECRET_ACCESS_KEY = ""

AWS_STORAGE_BUCKET_NAME = "my-mangoplateproject-bucket-2023-goldang"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.ap-northeast-2.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
```

- `AWS_STORAGE_BUCKET_NAME` : S3 저장소 이름
- `DEFAULT_FILE_STORAGE`와 `STATICFILES_STORAGE`는 위와 같이 지정한다.
- `AWS_S3_CUSTOM_DOMAIN` : 커스텀 도메인 경로. 위와 같이 하면 된다.
- `AWS_S3_FILE_OVERWRITE` : 같은 이름을 가진 파일이 업로드되었을 때 덮어쓸 것인가?
- `AWS_QUERYSTRING_AUTH` : URL로 액세스 키가 넘어가지 않도록

액세스 키는 발급받지 않아도 된다. IAM 역할을 EC2 인스턴스에 부여했기 때문인데, 발급받는 방법에 대해서는 다음 글들을 참고하라: Access Key 발급받기[^1].

`AWS_ACCESS_KEY_ID`와 `AWS_SECRET_ACCESS_KEY`를 제공하지 않으면 boto3은 내부적으로 IAM 정보를 통해 접근한다고 한다.[^4]

### supervisor, nginx 재시작
설정이 완료되었으면 EC2 인스턴스에서 해당 내용일 받아 `sudo systemctl restart supervisor`, `sudo service restart nginx`로 supervisor와 nginx를 재시작한다.

### collectstatic
```
python manage.py collectstatic
```
위 명령을 실행해 현재 어플리케이션이 사용하는 정적 파일들을 모아 S3에 업로드하고 배포 환경에서 사용하도록 한다. `collectstatic`을 여러번 실행하면, 변경된 파일만 적용되고 변경되지 않은 파일들은 그대로 유지되도록 작동한다.

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
	BASE_DIR / 'static',
]
```
정적 파일 경로가 위와 같이 설정되어 있음에도 `collectstatic` 실행시 설정된 S3 저장소로 정적 파일이 저장되고 사용된다.

<br>

---
# 참고자료
1. [Configure AWS S3 for static files - Cloud With Django](https://youtu.be/980gAjwR44I)
2. [Collectstatic to AWS S3](https://stackoverflow.com/questions/65962049/django-collectstatic-is-not-pushing-to-aws-s3)
3. [Django-storages official doc](https://django-storages.readthedocs.io/en/latest/)
4. [Django Staticfiels in S3 with IAM](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3)
5. [django-storages for Amazon S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
6. [Boto3 Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#credentials)
7. https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings


[^1]: [AWS Documentation - To get your access key ID and secret access key](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)
[^2]: [Using an IAM role to grant permissions to applications running on Amazon EC2 instances](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html?icmpid=docs_iam_console)
[^3]: [Grant my Amazon EC2 instance access to an Amazon S3 bucket](https://repost.aws/knowledge-center/ec2-instance-access-s3-bucket)
[^4]: https://stackoverflow.com/questions/46307447/use-django-storages-with-iam-instance-profiles 
[^5]: https://stackoverflow.com/questions/42141675/aws-s3-bucket-policy-to-block-access-to-all-but-one-directory-even-if-user-has