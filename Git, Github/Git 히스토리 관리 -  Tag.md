---
created_at : 2023-04-08, Sat
유효기록일 : 2023-04-08, Sat
topics : git tag
context : 
tags : git/히스토리_관리/tag
related : 
---
# Git Tag
## 태그 만들기
- `git tag <tag name>` : 현재 HEAD에 태그 등록
- `git tag <tag name> <commit hash>`
- `git tag -a <tag name> -m "message"`

<br>

## 태그 확인
- `git show (<tag name>)` : 모든(특정) 태그 내용 확인

<br>

## 태그 Push
> 태그는 따로 Push해야 전송된다.

- `gp origin <tag name>`
- `gp origin --tags` : 모든 태그 전송

<br>

## 태그 Checkout
> [!zsh 단축키]  
> `git checkout -b` : `gcb`  
> `git checkout` : `gco`

- `gcb <branch> <tag>` : 태그를 기반으로하는 브랜치로 체크아웃

<br>

## 태그 삭제
- `git tag -d <tag name>`

<br>

## 태그 이름 변경
- `git tag <새로운 이름> <기존 이름>` : 기존 이름을 가진 태그에 새로운 이름을 추가 -> 기존 이름 삭제

<br>

## 태그 보기
> 태그는 정렬되므로 고려해 태그이름을 작성

- `git tag -l`   리스트
- `git show-ref (--tags)` -> 연결된 해시키와 같이 보여줌

<br>

---
# 참고자료
- 멀티캠퍼스 Git & Github 실무 활용 - 5차시