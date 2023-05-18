---
created_at : 2023-05-04, Thu
유효기록일 : 2023-05-04, Thu
topics : 
context : 
tags : python/django/deploy aws/ec2
related : 
---
# 0. EC2 인스턴스 실행
❗️ **Root 계정으로 진행하지 않는다.**  보안상의 이유도 있고, 서비스를 잘못 실행해 초기화 해야 할 경우 하위 계정은 삭제후 다시 발급할 수 있지만 Root 계정은 쉽게 삭제하지 못할 수 있기 때문이다.

Root 계정(계정이 처음 만들어졌을때 Root 계정이다)을 사용하고 있는 경우 IAM → 사용자 → 사용자 추가를 선택해 하위 계정을 생성해 진행한다. AdministratorAccess 권한이면 충분하다. 직접 정책 연결할 수도 있고 권한이 지정된 그룹에 사용자를 추가할 수도 있다. 

IAM 맨 오른쪽 'AWS 계정' 섹션에서 기억하기 쉽도록 계정 별칭을 지정한다. 필자는 thebjko-alias로 지정했고, 유저명은 thebjko이다. 로그인 화면은 다음과 같다:

![[IAM 사용자로 로그인 1.png]]

<br>

![[IAM 사용자로 로그인 2.png]]

<br>

## 0. 보안 그룹  
### 1. 보안 그룹 생성
![[보안 그룹 생성.png]]

### 2. 기본 세부 정보 입력
![[기본 세부 정보 입력.png]]
VPC는 그대로 두면 된다.

### 3. 인바운드 규칙
EC2 인스턴스로 들어오는 트래픽에 대한 규칙. 모든 소스(0.0.0.0/0, IPv4)에서 HTTP와 SSH를 허용하고 진행한다.
![[인바운드 규칙.png]]

### 4. 아웃바운드 규칙
EC2 인스턴스에서 나가는 트래픽에 대한 규칙. 모든 소스(0.0.0.0/0, IPv4)로 HTTP를 허용한다.
![[아웃바운드 규칙.png]]

<br>

## 1. 인스턴스 만들기
### 1. 인스턴스 시작
![[인스턴스 시작.png]]

### 2. 이름을 지정하고 Ubuntu Server 22.04 LTS를 OS로 선택한다
![[AMI 선택.png]]

### 3. 인스턴스 유형은 프리 티어 사용이 가능한 t2.micro로 선택
![[인스턴스 유형 선택.png]]

### 4. 여기서는 키 페어 없이 진행한다.
![[키 페어 없이 계속 진행.png]]

### 5. 보안 그룹 선택
![[기존 보안 그룹 선택.png]]
기존 보안 그룹 선택 → 위에서 생성한 보안 그룹 선택

### 6. 인스턴스에 연결하기
![[인스턴스 선택 후 연결.png]]
![[EC2 Instance Connect.png]]
해당 인스턴스를 선택하고 연결→연결을 클릭한다.

<br>

# 1. 인스턴스 환경 설정
프로젝트 중 django-allauth 패키지를 사용했는데, 어떤 이유에선가 가상환경에서 설치가 안된다. [한 스택 오버플로우 답변](https://stackoverflow.com/questions/74065810/unable-to-install-django-allauth)에서는 파이썬 버전을 다운그레이드 하라고 하는데, pipenv라는 가상환경에서는 문제 없이 설치가 되어, 가상환경으로 pipenv를 사용하기로 한다.

<br>

## Pipenv는 파이썬 버전도 기록되는 것 같다. 따라서 인스턴스의 파이썬을 업그레이드한다.
💁 Ubuntu 22.04 LTS의 디폴트 파이썬 버전은 3.10.6이다. 이 버전 이하의 파이썬을 사용했다면 이 과정은 생략해도 좋을 것 같다.

1. `python`으로 `python3`를 호출하기 위한 패키지
```
sudo apt install python-is-python3
```
2. 파이썬 저장소 등록
```
sudo add-apt-repository ppa:deadsnakes/ppa
```
> `ENTER`

3. apt 업데이트 후 파이썬 3.11버전 설치
```
sudo apt update && sudo apt install python3.11 -y
```
4. `python3`으로 호출할 파이썬 지정
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 110 && sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 100 && sudo update-alternatives --config python3
```
실행 후 적절한 파이썬을 선택한다. 필자의 경우 2

5. 이후 `sudo apt-get update` 명령을 실행하면 `apt_pkg` 모듈이 없다는 에러가 뜰 것이다. 아래 명령을 실행해 현재 `apt_pkg`버전을 확인
```
cd /usr/lib/python3/dist-packages && ls -l | grep apt_pkg
```
6. 확인한 버전으로 아래 명령 실행
```
sudo ln -s apt_pkg.cpython-{확인한 apt_pkg 버전}-x86_64-linux-gnu.so apt_pkg.so
```
필자의 경우 310

<br>

## NGINX, supervisor 설치
```
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y nginx && sudo apt-get install supervisor
```

<br>

## Pip & pipenv 설치
Pip과 가상환경인 pipenv를 설치해야 한다. 파이썬 버전을 전면 개정했기 때문인 것 같다.

```
cd ~ && curl https://bootstrap.pypa.io/get-pip.py -O && python get-pip.py && . ~/.profile && pip install pipenv
```
홈 디렉토리로 이동해 pip 파일을 받고 실행 한다. `~/.profile` 파일을 실행해 `~/.local/bin` 디렉토리를 PATH에 추가해야 그 안에 있는 pip 명령을 바로 실행할 수 있다. 이후 `pip install pipenv`를 실행해 설치한다.

**홈 디렉토리**에서 가상 환경을 실행한다. (좀 더 구체적인 디버깅이 필요하겠지만, 특정 디렉토리에서 실행했을 때 잘 안 되던 것 같다는 기억이 있다. 홈 디렉토리에서 생성한 가상환경은 잘 작동했기 때문에 이 글에서는 홈 디렉토리에서 실행한 가상 환경에서 진행한다.)

프로젝트 디렉토리 생성 및 깃허브 클론 후 requirements.txt 파일을 사용해 필요 패키지들을 설치한다.

```
pipenv shell && pipenv install -r project/requirements.txt
```


<br>

# 2. Gunicorn.conf
`/etc/supervisor/conf.d` 디렉토리로 이동해 `gunicorn.conf` 파일을 생성한다.
```
cd /etc/supervisor/conf.d && sudo vi gunicorn.conf
```
슈퍼유저 권한으로 실행(`sudo`)해야 편집 가능하다. 아래와 같이 입력한다.
```python
[program:gunicorn]
directory=/home/ubuntu/{project 디렉토리}
command={gunicorn 커맨드가 있는 위치} --workers 3 --bind unix:/home/ubuntu/{project 디렉토리}/app.sock {어플리케이션 이름}.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn
```
- Gunicorn 커맨드가 있는 위치는 `whereis gunicorn` 커맨드로 확인할 수 있다. 이 프로젝트의 경우 `/home/ubuntu/.local/share/virtualenvs/ubuntu-iR9coyfD/bin/gunicorn`
- 어플리케이션 이름은 settings.py 파일의 `WSGI_APPLICATION`에서 확인할 수 있다. `'config.wsgi.application'`인 경우 `config`로 작성한다.
- 프로젝트 디렉토리 이름을 {project 디렉토리}에 입력한다

로그 파일이 저장될 장소를 생성한다
```
sudo mkdir /var/log/gunicorn
```

아래 명령으로 상태를 확인한다.
```
sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl status
```
RUNNING이 나오면 잘 작동한다는 뜻이다. 잘 안될경우 `sudo systemctl restart supervisor` 명령으로 supervisor를 재시작해보자.

<br>

# 3. Nginx.conf
아래 파일에서 user를 root이나 ubuntu로 수정하자. 
```
sudo vi /etc/nginx/nginx.conf
```
```
user root;
```

# 4. Django.conf
파일 생성 후
```
sudo vi /etc/nginx/sites-available/django.conf
```

아래 내용 작성
```
server{
    listen {사용할 포트 번호};
    server_name {접근할 주소. 띄어쓰기로 구분해 여러개 사용 가능};
                        
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/{project 디렉토리}/app.sock;
    }


}
```
- 사용할 포트 번호 : HTTP는 80
- EC2 인스턴스의 Public IPv4를 입력한다. Public IPv4 DNS도 같이 입력할 수 있는데, 이 때에는 nginx.conf 파일 http 블록 맨 위에 다음과 같이 내용을 추가할 필요가 있다:

/etc/nginx/nginx.conf:
```
http {
	server_names_hash_bucket_size  <size>;
	...
}
```
- Size : AWS EC2 인스턴스의 Public IPv4 DNS는 128로 충분하다.

<br>

# 5. Nginx 구문 테스트
```
sudo nginx -t
```
작성한 내용이 nginx 문법에 맞는지 검사한다.

<br>

# 6. `/etc/nginx/sites-enabled`에 django.conf에 대한 심볼릭 링크 생성 및 nginx restart
```
sudo ln /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled
```
- `ln` : `ln TARGET DIRECTORY`의 형태로 사용. TARGET에 대한 symbolic link를 DIRECTORY 안에 생성한다.

nginx 재시작
```
sudo service nginx restart
```

<br>

# 7. 기타
1. Disallowed Hosts 에러 : settings.py `ALLOWED_HOSTS` 리스트에 추가하고, 서버를 재부팅하거나 `sudo systemctl restart supervisor` 명령으로 supervisor만 다시 실행해 변경사항을 반영할 수 있다.
2. Migration 중 db가 잠겨있다고 뜰 수 있다. db를 삭제하고 다시 migrate를 진행해 해결할 수 있지만, 다른 방법도 알아볼 필요가 있을 것 같다.
3. conf 파일 수정후 supervisor reread, update, status 및 nginx를 재실행.
4. `mysqlclient`가 설치되지 않으면
	```
	sudo apt install -y python3.11-dev libmysqlclient-dev libssl-dev
	```

<br>

---
# 참고자료
- [PATH에 경로 추가하기](https://pimylifeup.com/ubuntu-add-to-path/)
- [Provided Domain Name Not Valid](https://notabela.hashnode.dev/how-to-solve-the-domain-name-provided-is-not-valid-according-to-rfc-10341035-in-django-during-development)
 - [Invalid HTTP Host Header](https://stackoverflow.com/questions/40582423/invalid-http-host-header)
 - [StackOverflow on django disallowedhost error](https://stackoverflow.com/questions/40565188/django-disallowedhost-error)
 - [linuxconfig](https://linuxconfig.org/how-to-restart-nginx-on-linux)
 - [subdomain wildcard](https://copyprogramming.com/howto/deploying-django-application-in-aws-raise-disallowed-host-exception)
 - https://stackoverflow.com/questions/50164501/unable-to-create-the-django-migrations-table-database-is-locked-error-when-cre
 - https://docs.djangoproject.com/en/4.2/ref/databases/#database-is-locked-errors
 - https://stackoverflow.com/questions/35657332/django-difference-between-using-server-through-manage-py-and-other-servers-like
- [Deploy a Django web app with Nginx to Amazon EC2 - Cloud With Django](https://youtu.be/7O1H9kr1CsA)
- [ln command](https://jjeongil.tistory.com/1408)
- [ln command linuxize](https://linuxize.com/post/how-to-create-symbolic-links-in-linux-using-the-ln-command/)
- [ln command man page](https://man7.org/linux/man-pages/man1/ln.1.html)
- [여러 server_name 지정하는 것에 관하여](https://nginx.org/en/docs/http/server_names.html)
- [무중단 배포](https://dadadamarine.github.io/java/spring/notification/project/2019/04/28/server-nginx-setting.html)
- [도메인 네임이 너무 길 경우](https://stackoverflow.com/questions/13895933/nginx-emerg-could-not-build-the-server-names-hash-you-should-increase-server)
- https://linuxhint.com/install-python-ubuntu-22-04/
- https://ubuntuhandbook.org/index.php/2022/10/python-3-11-released-how-install-ubuntu/
- https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux
- https://askubuntu.com/questions/1132349/terminal-not-opening-up-after-upgrading-python-to-3-7
- https://webisfree.com/2020-08-23/apt-%EC%84%A4%EC%B9%98%EB%90%9C-%ED%8C%A8%ED%82%A4%EC%A7%80-%EB%AA%A8%EB%93%88-%ED%99%95%EC%9D%B8%ED%95%98%EA%B1%B0%EB%82%98-%EC%B0%BE%EA%B8%B0
- [gunicorn.service](https://heuristicwave.github.io/pipenv01)
- [freedesktop - systemd](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [gunicorn systemd instead of supervisor](https://docs.gunicorn.org/en/stable/deploy.html#systemd)
- [`ModuleNotFoundError: No module named 'apt_pkg'`](https://stackoverflow.com/questions/13708180/python-dev-installation-error-importerror-no-module-named-apt-pkg)
	- [Why this happens](https://stackoverflow.com/questions/13708180/python-dev-installation-error-importerror-no-module-named-apt-pkg/64241654#64241654)
- [`mysqlclient`가 설치되지 않을 때](https://stackoverflow.com/questions/56133947/install-mysqlclient-via-pipenv-throw-errors)a