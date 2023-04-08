---
created_at : 2023-04-08, Sat
유효기록일 : 2023-04-08, Sat
topics : git reset
context : 
tags : git_reset, git_restore
related : git restore
---
# Reset
> `git reset <option> <commit_id>`

<br>

> [!Warning]  
> 주의해서 사용하세요

<br>

## Hard
> `git reset --hard <commit_id>` : `grhh <commit_id>`
> `git reset --hard HEAD^` : 현재 시점에서 커밋된 내용(unstaged)으로 돌아가기(한 단계 이전)

- 되돌린 이력 이후 내용 삭제
- Index 취소, add하기 전 상태(unstaged)
- 작업영역 파일 삭제

<br>

## Soft
> `git reset --soft HEAD^` : 커밋이 된 경우 커밋 이전으로 되돌리기  

- 이력 보존
- 인덱스, add한 상태 유지, 파일 모두 보존 -  **바로 다시 커밋 할 수 있는 상태로 남아있음**

<br>

## Mixed
> `grh --mixed`  
> 커밋한 내용을 unstaged 상태로 만들때 사용 (`git reset HEAD^`, `git reset HEAD~2` 최근 2개 커밋 unstage 하기 - *2개 커밋이 지워진다.* 숫자가 없으면 `^`와 같고 한단계 내려간다(하나가 지워진다).)  
> `git reset HEAD` : add 취소  
> 	`git reset HEAD <filename>` 또는 `git reset <filename>` : add하기 이전으로 되돌리기(staged -> unstaged). 내용 유지

- 디폴트 옵션
- 이력은 되돌리며 이후에 변경된 내용에 대해서는 남아있지만 인덱스는 초기화됨 (인덱스가 뭐여)
- 커밋하려면 다시 변경된 내용은 추가해야되는 상태
- Index 취소, add하기 전 상태(unstaged)로 돌아감
- 작업영역의 파일 보존

예시:
1. 파일 수정 후 add, commit
2. `grh <이전 commit_id>` 실행
3. 파일 내용은 그대로이면서 `Unstaged changes after reset:`라는 메세지와 함께 수정한 파일이 unstaged, modified 상태가 되어있다.
4. **커밋 자체만 취소** (히스토리 삭제)

<br>

# Restore
파일 수정 후 modified인 상태에서 `git restore` 실행시 수정한 내용이 사라진다. 커밋이 되지 않았기 때문에 **복구 불가**.

`--staged <filename>` : 수정 후 staged 된 파일들에 대해 실행시 unstaged 상태가 되고, 내용은 유지되어있다. `git reset <filename>`, `git reset HEAD <filename>`과 같다.

- `git reset --soft HEAD^` + `git restore --staged <filename>` + `git restore <filename>` = `git reset --hard HEAD^`

<br> 

---
# 참고자료
- 멀티캠퍼스 Git & Github 실무 활용 - 7차시

[^1]: