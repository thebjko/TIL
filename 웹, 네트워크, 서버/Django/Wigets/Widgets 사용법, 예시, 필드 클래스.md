---
created : 2023-04-03, Mon
topics : Widgets
context : django, python, ModelForm, Todo_ModelForm 프로젝트
tags : python/django/widget python/django/ModelForm
---
# [Widgets](https://docs.djangoproject.com/en/3.2/ref/forms/widgets/)
> 위젯은 html의 input 요소에 해당한다고 한다. html의 렌더링을 다루고, GET/POST 딕셔너리에서 각 위젯에 담당하는 데이터를 추출한다.

- [Built-in Field classes](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#built-in-field-classes) #python/django/fields

## 위젯 사용법
> 예시를 보며 익히자

0. 공식 문서
	```python
	from django import forms
	
	BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
	FAVORITE_COLORS_CHOICES = [
	    ('blue', 'Blue'),
	    ('green', 'Green'),
	    ('black', 'Black'),
	]
	
	class SimpleForm(forms.Form):
	    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
	    favorite_colors = forms.MultipleChoiceField(
	        required=False,
	        widget=forms.CheckboxSelectMultiple,
	        choices=FAVORITE_COLORS_CHOICES,
	    )
	```
	> `birth_year`는 `SelectDateWidget`을 위젯으로 갖는 `DateField` 타입의 필드이다. 선택지를 어떻게 입력하는지 눈여겨보자. `ModelForm`이 아닌 그냥 `Form`을 사용하므로 속성에 디폴트로 적용되는 필드 클래스가 없다.

1. Todo_ModelForm/todos/forms.py
	```python
	from django import forms
	from .models import Todo
	from datetime import datetime
	
	class TodoForm(forms.ModelForm):
	    title = forms.CharField(
	        label='할 일',
	        widget=forms.TextInput(
	            attrs={
	                'id': 'title',
	                'placeholder': '제목을 입력하세요',
	                'class': 'form-control',
	            },
	        ),
	    )
	    content = forms.CharField(
	        label='세부사항',
	        widget=forms.Textarea(
	            attrs={
	                'id': 'content',
	                'class': 'form-control',
	                'placeholder': '세부사항을 입력하세요',
	            },
	        ),
	    )
	    completed = forms.BooleanField(
	        label='완료여부',
	        required=False,
	        widget=forms.CheckboxInput(
	            attrs={
	                'id': 'completed',
	            }
	        )
	    )
	    priority = forms.ChoiceField(
	        label='우선순위',
	        label_suffix='',
	        initial=3,
	        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],   # (html_value, 보이는 값)
	        widget=forms.Select(
	            attrs={
	                'id': 'priority',
	            },
	        ),
	    )
	    # priority = forms.IntegerField(
	    #     widget=forms.NumberInput(
	    #         attrs={'min': 1, 'max': 5, 'value': 3},
	    #     )
	    # )
	    deadline = forms.DateField(
	        label='기한',
	        label_suffix='',
	        initial=datetime.today(),
	        widget=forms.DateInput(
	            attrs={
	                'id': 'deadline',
	                'type': 'date',
	            },
	        ),
	    )
	
	    class Meta:
	        model = Todo
	        fields = '__all__'
	        
	```
	> priority 필드를 `ChoieField`로 오버라이드(모델은 `IntegerField`를 사용하며 모델폼의 디폴트 필드 또한 `IntegerField`), 위젯은 [[각 모델 필드와 해당하는 디폴트 필드 타입 | ChoiceField의 디폴트 위젯]]인 `Select`를 사용하고, `attrs`로 최소 최대, 기본값을 주는 대신 `ChoiceField`의 속성을 사용했다.  

	```python
		deadline = forms.DateField(
	        label='기한',
	        label_suffix='',  # 콜론 없어짐
	        initial=datetime.today(),   # 오늘 날짜로 디폴트 값 설정
	        widget=forms.DateInput(
	            attrs={
	                'id': 'deadline',
	                'type': 'date',
	            },
	        ),
	    )
	```
	> `label_suffix`, `initial`와 같은 필드 속성을 사용해 적절한 html 속성을 부여할 수 있다.


	django - fields.py
	```python
	class Field:
	    widget = TextInput  # Default widget to use when rendering this type of Field.
	    hidden_widget = HiddenInput  # Default widget to use when rendering this as "hidden".
	    default_validators = []  # Default set of validators
	    # Add an 'invalid' entry to default_error_message if you want a specific
	    # field error message not raised by the field validators.
	    default_error_messages = {
	        'required': _('This field is required.'),
	    }
	    empty_values = list(validators.EMPTY_VALUES)
	
	    def __init__(self, *, required=True, widget=None, label=None, initial=None,
	                 help_text='', error_messages=None, show_hidden_initial=False,
	                 validators=(), localize=False, disabled=False, label_suffix=None):
		    ...
	```
	> [CharField에 label이라는 속성이 없지만](https://docs.djangoproject.com/en/3.2/_modules/django/forms/fields/#CharField) `CharField`가 상속하는 `Field` 클래스의 속성을 사용한다. 템플릿에서 점 표기법(`{{ field.label }}`)으로 접근 가능하다.
 ^0dce50
2. Django `AuthenticationForm`
	```python
	class AuthenticationForm(forms.Form):
	    """
	    Base class for authenticating users. Extend this to get a form that accepts
	    username/password logins.
	    """
	    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
	    password = forms.CharField(
	        label=_("Password"),
	        strip=False,
	        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
	    )
	    ...
	```
	> password의 `CharField`가 위젯을 `PasswordInput`으로 커스터마이징을 하며, ([`CharField`의 디폴트 위젯은 `TextInput`이다](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#charfield)) `attrs`에 `autocomplete` 속성 값을 `current-password`로 주고 있다.

어떤 위젯들이 있는지, 어떻게 사용하는지 훑어보고 필요할 때 마다 문서를 보며 적용하면 될 것 같다.

[폼 필드 메서드, 속성](https://docs.djangoproject.com/en/3.2/ref/forms/fields/#module-django.forms.fields). 또한 소스코드를 통해 어떤 속성, 메서드들이 존재하는지 훑어보고 필요할 때 문서로 디테일을 확인하면 될 것 같다(ex. `has_changed()`) #python/django/forms/fields

---
# 참고자료
- Django 공식문서 3.2버전