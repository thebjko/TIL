---
created_at : 2023-05-05, Fri
유효기록일 : 2023-05-05, Fri
topics : 
context : linux, ubuntu
tags : brave_browser linux ubuntu
related : 
---
# `Skipping acquire of configured file 'main/binary-i386/Packages' as repository 'https://brave-browser-apt-release.s3.brave.com stable InRelease' doesn't support architecture 'i386'`
[설치 명령](https://brave.com/linux/#debian-ubuntu-mint) 중 세번째 명령에 arch=arm64 아래와 같이 추가:
```
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list
```

<br>

# `ModuleNotFoundError: No module named 'apt_pkg'`
![[Django 어플리케이션 AWS EC2 인스턴스로 배포하기#Pipenv는 파이썬 버전도 기록되는 것 같다. 따라서 인스턴스의 파이썬을 업그레이드한다.]]
여기서  5, 6 번 진행.

<br>

# `Could not get lock /var/lib/dpkg/lock-frontend`

```
sudo killall apt apt-get

# 또는
sudo rm /var/lib/apt/lists/lock  
sudo rm /var/cache/apt/archives/lock  
sudo rm /var/lib/dpkg/lock*
```
이후 
```
sudo dpkg --configure -a
```
다시 apt update를 시도하면 해결.
```
sudo apt update
```

<br>

---
# 참고자료
1. https://kgu0724.tistory.com/71
2. https://community.brave.com/t/solved-linux-deb-install-gives-error-when-you-apt-update-a-repository/464626
