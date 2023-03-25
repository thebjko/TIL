---
date:  2023-03-23, Thu
subject: git, github, rebase
tags: 
context: 
---
> Do not rebase commits that exist outside your repository and that people may have based work on. 본인 소유가 아닌 저장소에서나 다른 사람이 작업의 기초로 삼는s 저장소에서는 rebase 하지 말 것.

# [`git rebase`](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)

## Rebasing
> You can take the patch of the change that was introduced in C4 and reapply it on top of C3. In Git, this is called **rebasing**.

하나에 커밋에서 갈라져나온 두 개의 브랜치 중 하나의 브랜치(`main`이라 하자)에서 다른 브랜치(`test`라 하자)의 변경 사항을 현재 브랜치 위에 적용하는 방법이라고 설명한다. 

```zsh
# test 브랜치로 이동
git checkout test

# main 브랜치의 커밋을 test 브랜치에 rebase 하기
git rebase main

```

예를 들어
main 브랜치에 test.txt를 만들고 test 브랜치 생성 후 이동 및 test-branch.txt 생성, main 브랜치로 돌아와 main-branch.txt 생성

test 브랜치에 test.txt와 test-branch.txt가 있으며, main 브랜치에 test.txt와 main-branch.txt 파일이 있다. 이후 test 브랜치에서 git rebase main 명령 실행 -> test 브랜치에 main-branch.txt 파일이 새로 생겼다. 깃허브 공식 문서에서는 여기서 main 브랜치에서 test 브랜치를 merge하면 내용은 rebasing 없이 merge한 것과 같지만, 히스토리가 훨씬 더 깔끔하다고 한다.

## 실험해보기
> 같은 파일 내용이 다를 경우엔?  

main브랜치:
- test.txt
- 1.txt

test 브랜치:
- test.txt
- 1.txt

1. main 브랜치에서 1.txt 생성 후 test 브랜치를 만들었고, 내용은 동일하다.
2. 브랜치가 갈라진 후에 각 브랜치에서 test.txt를 생성했으며, main 브랜치의 test.txt의 내용은 "main", test 브랜치의 test.txt의 내용은 "test"이다.
3. 각 브랜치의 test.txt에 다른 내용을 추가하고 test 브랜치에서 `git rebase main` 실행

컨플릭트가 생겼다.
```zsh
Alias tip: grb main
Auto-merging test.txt
CONFLICT (content): Merge conflict in test.txt
error: could not apply 01239ba... test.txt 수정
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
Could not apply 01239ba... test.txt 수정
```
그리고 브랜치 명이 해시 값과 같이 되었다.

### 세 가지 옵션
1. `git add/rm <conflicted_files>` 후 `git rebase --continue`
2. `git rebase --skip` : 스킵하기
3. `git rebase --abort` : 리베이스 버리기

#### 1번
> `git add/rm <conflicted_files>` 후 `git rebase --continue`

```
1 <<<<<<< HEAD
2 main
3 =======
4 test
5 >>>>>>> 01239ba (test.txt 수정)
```
파일 내용이다.
`git rebase --continue`까지 실행하면 `Successfully rebased and updated`라는 시지와 함께 원래 브랜치로 돌아온다. 파일 내용은 위와 같이 되었다.

#### 2번
> `git rebase --skip`

`Successfully rebased and updated refs/heads/test.`라는 메세지가 떴고, test 브랜치의 test.txt 파일이 main 브랜치의 test.txt 파일과 같아졌다.

> [!Note]  
> 여기서 test.txt 파일 내용을 다시 "test"로 수정하고 `git rebase main`을 실행했으나 `Current branch test is up to date.`라는 메세지가 뜬다. 이 기능이 있어야 매번 이미 정리된 rebase에 대해 컨플릭트를 다시 해결해야 하지 않을 수 있다. 예를 들어, pull 받은 수업 내용에 대해 내가 정리한 내용을 유지하는 방향으로 컨플릭트를 해결했는데, 다음날 다시 pull 받은 수업 내용에 대해 다시 컨플릭트를 해결해야 한다면, 사실상 rebase는 쓸모가 없을 것이다.

#### 3번
> `git rebase --abort`

그래서 test2.txt 파일을 다시 만들고 위 명령을 실행해보기로 한다. 각 파일의 내용은 test.txt의 처음 내용과 같다. 

`git rebase --abort`는 rebase 하기 이전으로 되돌리는 명령이다. 각 파일의 내용이 유지되었고, `git rebase main`을 다시 실행할 경우, 컨플릭트가 발생했다는 메세지가 뜬다.


## Rebase vs. Merge
### 커밋 히스토리를 보는 두가지 관점:
1. 무엇이 실제로 일어났는지에 대한 기록(a record of what actually happened)
2. 프로젝트가 어떻게 만들어졌는지에 대한 이야기(the story of how your project was made)

2번의 관점에서 rebase나 filter-branch를 사용하면, 커밋 히스토리를 깔끔하게 정리할 수 있다. merge를 더 공부하면서 비교해야겠지만 일단은 "둘 다 브랜치를 합치는 방식이고, merge는 충돌 기록을 남기며, rebase는 남기지 않는다" 정도로 이해해야겠다.


---

# 더 공부해 볼 주제
- [More Interesting Rebases](https://git-scm.com/book/en/v2/Git-Branching-Rebasing#_more_interesting_rebases)