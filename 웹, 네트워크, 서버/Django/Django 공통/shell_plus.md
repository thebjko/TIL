---
created : 2023-03-28, Tue
topics : shell_plus, ipython, jupyter notebook
context : django, python
---
# shell_plus
## 설치
```zsh
pip install ipython django-extensions
```
Jupyter Notebook을 사용하려면 [[shell_plus with Jupyter Notebook|이 글]]을 참고.

`settings.py` :
```python
INSTALLED_APPS = [
	'django_extensions',   # 하이픈이 아니라 언더스코어
]
```

## 실행
```zsh
python manage.py shell_plus
```

> 이제 인터랙티브 셸에서 장고를 사용할 준비가 되었다.

