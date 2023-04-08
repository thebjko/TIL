---
created_at : <% tp.file.creation_date("YYYY-MM-DD, ddd") %>
유효기록일 : <% tp.date.now("YYYY-MM-DD, ddd") %>
topics : 
context : zsh
tags : git_merge, git_rebase, git_branch, git_checkout
related : 
---
# Branch
- `gb --all` : remote 브랜치 목록을 포함한 모든 브랜치 목록

<br>

## 원격 브랜치 가져오기
- `gcb <local_branch> <remote_branch>` : remote_branch -> `origin/...`

<br>

# Merge
## Diff - 브랜치 비교하기
- `git diff <원본> <대상>`
- `git diff main origin/main` : 원격 브랜치에도 가능
- `git merge main origin/main`

<br>

## Conflict (충돌)
- `git merge --abort` : 병합 취소
- 파일 수정 후 add, commit

<br>

# Rebase
> [[git rebase]]와 같이 보기  
> 이력을 하나의 줄기로 만든다

예시:
1. \[main\] : hello.txt 생성 후 issue 브랜치 분기
2. \[issue\] : hello1.txt 생성
3. \[main\] : hello.txt 수정
4. \[issue\] : `grb main` 및 `g log` 확인 -> 커밋 히스토리 순서가 1, 3, 2이다.
5. \[main\] : `g log` -> 아직 1, 3
6. \[main\] : `gm issue` -> issue 브랜치가 병합되었고 커밋 히스토리 순서는 1, 3, 2이다.

만약 4번 단계에서 rebase가 아니라 병합을 한다면 컨플릭트가 발생하고 issue 브랜치의 커밋 히스토리 순서는 '1, 2, 3 + 머지 커밋'이다. Main 브랜치로 체크아웃 후 병합시 커밋 히스토리는 issue 브랜치와 같아진다.


---
# 참고자료
- 멀티캠퍼스 Git & Github 실무 활용 - 6차시

[^1]: