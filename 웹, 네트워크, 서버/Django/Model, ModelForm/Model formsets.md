---
created : 2023-04-03, Mon
topics : Model formsets
context : django, python
---
# [Model formsets](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#model-formsets)
> A [formset](https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#formsets) is a layer of abstraction to work with multiple forms on the same page. It can be best compared to a data grid.  
> Set of `ModelForm`?
> 그냥 `FormSet`과 비슷하다고 한다. 어떻게 다르지?

```python
>>> from django.forms import modelformset_factory
>>> from myapp.models import Author
>>> AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))

>>> AuthorFormSet = modelformset_factory(Author, exclude=('birth_date',))

>>> formset = AuthorFormSet()
>>> print(formset)
<input type="hidden" name="form-TOTAL_FORMS" value="1" id="id_form-TOTAL_FORMS"><input type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS"><input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS"><input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS">
<tr><th><label for="id_form-0-name">Name:</label></th><td><input id="id_form-0-name" type="text" name="form-0-name" maxlength="100"></td></tr>
<tr><th><label for="id_form-0-title">Title:</label></th><td><select name="form-0-title" id="id_form-0-title">
<option value="" selected>---------</option>
<option value="MR">Mr.</option>
<option value="MRS">Mrs.</option>
<option value="MS">Ms.</option>
</select><input type="hidden" name="form-0-id" id="id_form-0-id"></td></tr>
```

## [Using a custom queryset](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#using-a-custom-queryset)
> `queryset` 인자를 할당해 원하는 `ModelFormSet` 인스턴스를 생성하는 방법

```python
from django.forms import modelformset_factory
from django.shortcuts import render
from myapp.models import Author

def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
    if request.method == "POST":
        formset = AuthorFormSet(
            request.POST, request.FILES,
            queryset=Author.objects.filter(name__startswith='O'),
        )
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
    return render(request, 'manage_authors.html', {'formset': formset})
```

## [Using the formset in the template](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#using-the-formset-in-the-template)
> 실제로 구현해보지 않으면 와닿지 않을 것
> 더 내려보니 inline으로도 구현가능하다고 한다.

아래와 같이 사용하는 걸로 봐서 여러 Form 객체를 담고 있는 객체로 이해할 수 있을 것 같다.
```python
<form method="post">
    {{ formset.management_form }}
    {% for form in formset %}
        {{ form.id }}
        <ul>
            <li>{{ form.name }}</li>
            <li>{{ form.age }}</li>
        </ul>
    {% endfor %}
</form>
```

