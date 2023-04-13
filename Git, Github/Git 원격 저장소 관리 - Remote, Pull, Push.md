---
created_at : 2023-04-13, Thu
유효기록일 : 2023-04-13, Thu
topics : 
context : 
tags : git/remote git/pull git/push git/stash
related : 
---
# Git Remote

- `git remote add <name> <url>` : 원격 저장소 추가하기. name에 보통 origin을 쓴다 
- `git remote -v` (`git remote --verbose`) : 원격 저장소 목록 보기

<br>

원격 저장소 갱신(원격 저장소의 내용을 로컬에 갱신)
- `git remote update`
- `git remote prune origin`
- `git fetch --prune`

<br>

원격에서 삭제된 브랜치 업데이트(???)
- `git remote prune origin`
- `git remote update --prune`

<br>

원격 저장소 브랜치 확인
- `git branch -r` (`git branch --remotes`)
- `git branch -a` (`git branch --all`) : 로컬, 리모트 모두 확인

<br>

원격 저장소의 브랜치 가져오기
- `git checkout -t origin/main` : origin이라는 이름의 원격 저장소의 master 브랜치를 가져와서 동일한 이름으로 로컬 저장소 브랜치 생성 후 체크아웃.
- `git checkout -b master2 origin/master` : 가져온 후 브랜치 이름을 master2로 변경해 생성하고 체크아웃. (다시 푸시할때는 어떻게? `gp origin main2`라고 하면 `origin/main`에 푸시가 되나?)
- `git checkout origin/main` : 로컬에 받아서 확인/테스트 가능, 커밋/푸시 불가. 체크아웃시 사라짐.

<br>

# Pull
📝 원격 저장소의 내용을 로컬 저장소에 갱신. (fetch + merge)
- `git pull --rebase origin main` : 가져와 rebase 한다.
- `git pull --rebase=preserve origin main` : 가져온 커밋 뒤에 새로운 커밋 추가 (???)

<br>

# Push
📝 로컬 저장소의 변경 내용을 원격 저장소로 보냄
- `git push --set-upstream origin main` : 업스트림 브랜치 지정. 향후 main 브랜치 푸시의 대상을 명시한다. 한번만 하면 된다.
- `git push origin <다른 브랜치명>` : 다른 브랜치를 전송
- `git push origin HEAD : main`
	- origin : 원격 저장소 이름
	- HEAD : 전송할 최종 커밋
	- main : 원격 저장소 브랜치 이름

<br>

강제 푸시(Force Push)
> 원격 저장소에 main 브랜치의 내용이 반영된다.

- `gp --force origin HEAD : main` 
- `gp origin +HEAD : main`

<br>

원격 브랜치 삭제
- `gp --delete origin feature` : origin 저장소의 feature 브랜치를 삭제한다. 
- `gp [remotename] [:branch]` : 위와 같다.
- `gp [remotename] [localbranch] [:remotebranch]` : localbranch와 remotebranch가 연결되어있음을 명시

<br>

충돌시 push하지 않기
- `gp --force-with-lease origin main`

<br>

# Fetch
📝 원격 저장소의 내용을 내려받기만 한다. 로컬 브랜치에 반영하려면 명시적으로 merge를 해야 함.
- `git fetch origin <branch>` : 원격 저장소의 `<branch>` 가져오기. `<branch>` 생략시 모든 브랜치 가져오기.
- `git fetch origin main && git merge origin/main` = `git pull origin main`

<br>

⭐️ 원격 저장소의 데이터를 가져온 후 로컬의 브랜치가 원격의 이력을 가지도록 변경
- `git fetch origin main && git reset --hard origin/main`

<br>

# 원격 저장소 관리
- `git remote show [remotename]` : 살펴보기
- `git remote rename [대상 이름] [새로운 이름]` : 이름 변경
- `git remote rm [remotename]` : 삭제

<br>

# Stash
- 커밋하지 않고 나중에 다시 돌아와서 작업을 수행하기 위해 현재 상태를 저장.
- 워킹 디렉토리(?)에서 수정한 파일만 저장.
- Modified tracked 파일과, staging area에 있는 파일을 보관.
- 아직 끝나지 않은 수정사항을 stack에 잠시 저장.

<br>

명령어들
- `git stash list` : 목록 보기
- `git stash save` : 현재 작업을 저장하고 브랜치를 HEAD로 이동(hard)
- `git stash pop` : 가장 최근에 저장한 stash가 현재 브랜치에 적용됨. Stash는 stack에서 제거.
- `git stash apply` : Stack에서 pop 하지 않고 현재 브랜치에 가장 최근에 저장한 stash를 현재 브랜치에 적용.
- `git stash apply stash@{0}`
- `git stash drop` : 모두 삭제
- `git stash drop stash@{0}`
- `git stash clear` : drop과 다른점???

⭐️ Stash 저장 후 계속 작업하다가 다시 stash를 적용할 때 충돌이 날 수 있다. 하지만 `git stash branch <branch>` 를 사용해 stash 할 당시의 커밋 + stash했던 내용으로 브랜치를 만들 수 있다. 

<br>

---
# 참고자료
- 멀티캠퍼스 Git & Github 실무 활용 - 9차시

[^1]: