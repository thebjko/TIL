---
created_at : 2023-04-10, Mon
유효기록일 : 2023-04-10, Mon
topics : git revert
context : 
tags : git_revert
related : 
---
# Git 작업 취소 - Revert
> 돌아가려는 커밋으로 저장소 재설정. 해당 커밋 이후 이력은 유지, 새로운 커밋이 만들어짐.

- `git revert HEAD` : 한 단계 이전으로 롤백 (`^`, `~` 차이?)
- `git revert <commit_id>` : 해당 시점으로 롤백

<br>

## 수정 전으로 되돌리기
- `git checkout filename` : checkout을 이렇게도 사용할 수 있다.

<br>

## 파일 삭제
- `git rm filename` : 파일 삭제
- `git reset HEAD filename` : 파일 삭제 취소 ^0f27f3
- `git rm --cached filename` : 파일 삭제해 Unstaged 상태로 만들기 (작업 영역에 남겨 놓음)

<br>

## 파일 이름 변경
- `git mv filename filename2` - 아래와 같은 효과를 낸다.
	```zsh
	mv filename filename2
	git rm filename
	git add filename2
	```

<br>

## 파일 복구
- [[Git 작업 취소 - Revert#^0f27f3|파일 삭제 취소]]
- `git checkout [files]` : 삭제된 파일 복구(`[files]`?)
- `git ls-files -d | xargs git checkout --` : 삭제된 모든 파일 복구 (`git ls-files -d` : 삭제된 파일 리스트 보기)

<br>

## Unstaged 파일 삭제
- `git clean` : 추적중이지 않은 파일만 삭제(.gitignore에 명시된 파일 제외)
- `git clean -f` : 파일만 삭제(디렉토리 제외)
- `git clean -f -d` : 파일과 디렉토리 삭제
- `git clean -f -d -x` : .gitignore에 명시된 파일까지 삭제
- `git clean -n -f` : 미리 실행해보고 어떤 파일이 지워지는지 알려줌

---

# 실습

## revert 실습

1. a 추가 후 커밋
2. b 추가 후 커밋
3. c 추가 후 커밋
4. `git revert HEAD^1` 실행시 아래와 같은 메세지가 뜬다.
	```zsh
	Auto-merging abc.txt
	CONFLICT (content): Merge conflict in abc.txt
	error: could not revert 4a37dae... b
	hint: After resolving the conflicts, mark them with
	hint: "git add/rm <pathspec>", then run
	hint: "git revert --continue".
	hint: You can instead skip this commit with "git revert --skip".
	hint: To abort and get back to the state before "git revert",
	hint: run "git revert --abort".
	```

5. 파일 내용을 확인해보니 아래와 같다
	```
	a
	<<<<<<< HEAD
	b
	c
	=======
    >>>>>>> parent of 4a37dae (b)
	```

    > HEAD^1 실행시 두 단계(b, c)가 삭제되고 a 만 있던 상태로 돌아가려한다.  
    > Incoming Status 저장 -> Revert "b"라는 커밋 메세지와 함께 "b"를 입력하기 이전으로 돌아간다.

의아한 점은 `git revert --continue`가 아니라 커밋을 해야 됐다는 점이다. 나중에 다시 확인해 볼 필요가 있다.

<br>

## 삭제 실습
1. `git rm abc.txt` : 파일 삭제 (staged : `deleted: abc.txt`)
2. `git reset HEAD abc.txt` : abc.txt를 한 단계 되돌림([[Git 작업 취소 - Reset|mixed]])  -> `deleted: abc.txt`가 unstaged 된다.
3. `git restore abc.txt` : unstaged 파일들을 복구함 -> 삭제된 abc.txt가 다시 복구되었다.

<br>

## 복구 실습
- `git rm`으로 a 삭제 -> staged
- `git ls-files -d`로 확인 안됨 : 강의 내용과 다른 점이다.
- `git reset HEAD a` 이후 확인됨
- 이후 `git checkout a`로 복구됨
- `git checkout *`나 `git restore --staged *` 처럼 와일드카드를 사용할 수 없다.

<br>

## Unstaged 삭제 실습
- `git clean -d`만 사용할 수 없다. `git clean -f -d`를 사용해야함

<br>

---
# 참고자료
- 멀티캠퍼스 Git & Github 실무 활용 - 8차시

[^1]: