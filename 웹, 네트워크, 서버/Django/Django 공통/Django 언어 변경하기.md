---
created : 2023-03-24, Fri
topics : django language change
context : django, settings
---
# Django 언어 변경하기
[international language code](http://www.lingoes.net/en/translator/langcode.htm)를 참고해 언어 코드를 가져온다. 아래의 두 코드 모두 한국어로 번역된 admin 페이지를 보여준다.
```python
LANGUAGE_CODE = 'ko'
LANGUAGE_CODE = 'ko-kr'
```