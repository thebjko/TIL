---
created : 2023-04-03, Mon
topics : Form 클래스로 만든 Form에 속성 추가하기
context : django, python
---
# Form 클래스로 만든 Form에 속성 추가하기
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