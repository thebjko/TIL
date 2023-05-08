---
created_at : 2023-05-06, Sat
유효기록일 : 2023-05-06, Sat
topics : 
context : 
tags : aws access_key
related : 
---
# AWS ACCESS KEY 발급받기
1. IAM(Identity and Access Management) 서비스 맨 왼쪽 사이드바에서 '사용자' 선택
!['사용자' 선택](https://velog.velcdn.com/images/thebjko/post/cb146ef1-0dfe-42e5-b3bb-c27af62f62ed/image.png)

2. 키를 발급할 사용자 이름 선택
![사용자 이름 선택](https://velog.velcdn.com/images/thebjko/post/cff963e7-2add-4cfb-94f3-8668e07f547d/image.png)

3. 보안 자격 증명 탭 클릭
![보안 자격 증명 탭 클릭](https://velog.velcdn.com/images/thebjko/post/df88b302-63c8-431e-ae50-2cbaad7d6ddd/image.png)

4. 액세스 키 만들기 클릭
![액세스 키 만들기 클릭](https://velog.velcdn.com/images/thebjko/post/c83abbc6-ad8a-4ad6-89fd-fa684a4fe008/image.png)

5. 로컬에서 사용할 키를 발급받는 중이므로 '로컬 코드'를 선택하고, IAM 대신 발급받는다는걸 이해한다는 표시로 아래 체크 후 다음 클릭
![액세스 키 모범 사례 및 대안](https://velog.velcdn.com/images/thebjko/post/950a5501-6ed7-4eba-b029-91e104fa4485/image.png)

6. 태그(선택사항) 지정 후 액세스 키 만들기 클릭
![태그(선택사항) 지정 후 액세스 키 만들기 클릭](https://velog.velcdn.com/images/thebjko/post/199c7b5c-b487-4500-8a0c-bba80bc3153a/image.png)

7. 액세스 키는 다시 확인 불가하니 잘 저장하도록 하자. csv 파일로 다운받아 저장할 수도 있다.
![액세스 키 저장](https://velog.velcdn.com/images/thebjko/post/8b2803aa-b2c4-4ab4-98ae-edef4f04a793/image.png)

---
# 더 공부하기
- [AWS 공식문서 - IAM](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_credentials_access-keys.html)