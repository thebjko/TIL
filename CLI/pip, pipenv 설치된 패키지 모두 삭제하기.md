---
created_at : 2023-04-18, Tue
유효기록일 : 2023-04-18, Tue
topics : 
context : 
tags : pip pipenv
related : 
---
# 설치된 패키지 모두 삭제하기 (pip)
- `pip freeze | xargs pip uninstall -y` 
	- `pip freeze | xargs pipenv uninstall -y`는 안됨
- `pipenv uninstall --all`

<br>

---
# 참고자료
- https://stackoverflow.com/questions/11248073/how-do-i-remove-all-packages-installed-by-pip
- https://stackoverflow.com/questions/59446588/how-do-you-uninstall-multiple-packages-with-pipenv
- https://www.activestate.com/resources/quick-reads/how-to-uninstall-python-packages/