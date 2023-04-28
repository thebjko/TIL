---
created_at : 2023-04-19, Wed
유효기록일 : 2023-04-19, Wed
topics : 
context : 
tags : python/django/fixtures database
related : 
---
# Django DB에 초기 데이터 제공하기

## `python manage.py dumpdata --indent 2 articles.article`
- `dumpdata` : 데이터 추출하기
- `--indent 2` : JSON 들여쓰기 간격 2. 지정하지 않으면 1줄이 생성된다.
- `articles.article` : articles 앱의 article 모델에서 데이터 추출

<br>

## `python -Xutf8 manage.py loaddata articles.json users.json comments.json`
- `-Xutf8` : 파일 인코딩 형식을 utf8로 지정
- `loaddata` : fixture 파일로 DB에 데이터 쓰기
- `articles.json users.json comments.json` : 어플리케이션 fixtures 디렉토레의 fixture 파일들.

<br>

---
# 참고자료
- 하이퍼그로스 교육자료

[^1]: