---
created : 2023-04-03, Mon
topics : ModelForm 클래스로 만든 Form에 속성 추가하기
context : django, python
---
# ModelForm 클래스로 만든 Form에 속성 추가하기
> `Form` 클래스에서 추가하려는 속성에 대한 클래스 변수를 만들고 `widget`을 사용한다.

```python
class ArticleForm(forms.ModelForm):
    title = forms.CharField(
	    label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title',
                'placeholder': '제목을 입력해주세요',
            }
        )
    )

    class Meta:
        model = Article
        fields = "__all__"


```

# 더 공부해 볼 것
- [[클래스 변수는 인스턴스 변수 생성 전에 생성된다|각 페이지별 다른 속성 적용하기]]