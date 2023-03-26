---
created : 2023-03-26, Sun
topics : git, gitignore
context : 
---
# `!`
```
# Ignore everything
*

# Except
!.gitignore

# even if they are in subdirectories
!*/

# files in subdirectories
!*/a/b/file1.txt
!*/a/b/c/*
```

---
# 참고자료
- [Make .gitignore ignore everything except a few files](https://stackoverflow.com/questions/987142/make-gitignore-ignore-everything-except-a-few-files)