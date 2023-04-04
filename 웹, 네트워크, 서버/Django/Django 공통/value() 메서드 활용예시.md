---
created : 2023-04-03, Mon
topics : value() 메서드 활용예시
context : django, python, ModelForm
---
# [Providing initial values()](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#providing-initial-values)
아래는 제목 링크에서 가져온 예시이다.

```python
>>> article = Article.objects.get(pk=1)
>>> article.headline
'My headline'
>>> form = ArticleForm(initial={'headline': 'Initial headline'}, instance=article)
>>> form['headline'].value()
'Initial headline'
```

기본 값으로 `ArticleForm`을 만들고, `form['headline'].value()`로 `article`과 `headline`만 다르게 만들어진 새로운 `ArticleForm` 인스턴스의 `headline` 값을 확인한다.