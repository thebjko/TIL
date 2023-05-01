---
created_at : 2023-04-29, Sat
유효기록일 : 2023-04-29, Sat
topics : 
context : Auth_2
tags : python/django/CBV FormView
related : 
---
# Form handling with class-based views

## 일반 Form을 사용하는 경우
먼저 일반 Form(AuthenticationForm)을 사용하는 로그인 뷰함수를 리팩터해보자.
```python
def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```

```python
class LoginFormView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form) -> HttpResponse:
        auth_login(self.request, form.get_user())
        return super().form_valid(form)
```
슥슥 구현한 뒤 `form_valid` 메서드 안에서 `auth_login` 함수를 호출한다. request는 self에서 받아온다.

<br>

## ModelForm을 사용하는 경우
CreateView, UpdateView, DeleteView를 사용하라고 한다.

다음은 signup 뷰함수이다:
```python
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')   # 프로젝트 index
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```

```python
class SignupCreateView(CreateView):
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('index')
    form_class = CustomUserCreationForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        auth_login(self.request, form.get_user())
        return super().form_valid(form)
```
위와 같이 바꾸면 회원가입시 바로 로그인이 될 줄 알았는데, `'CustomUserCreationForm' object has no attribute 'get_user'`라는 오류메세지가 떴다. 

`form_valid` 메서드를 약간 수정했다.
```python
	def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        # valid = super().form_valid(form)
        auth_login(self.request, self.object)
        return super().form_valid(form)
```
form.save()했다고 해서 바로 로그인이 되지 않았다(`'AnonymousUser' object has no attribute '_meta'`). 
```python
	def form_valid(self, form: BaseModelForm) -> HttpResponse:
        valid = super().form_valid(form)
        auth_login(self.request, self.object)
        return valid
```
로그인 뷰와는 다르게 먼저 부모클래스의 `form_valid`메서드를 실행한 후에야 로그인이 되었다.

<br>

---
# 참고자료
- https://stackoverflow.com/questions/27771079/how-to-login-a-user-automatically-after-registration-in-formview-with-django
- https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView
- https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-editing/
- https://stackoverflow.com/questions/68388839/how-to-login-automatically-after-signup-in-django-class-base-view

[^1]: