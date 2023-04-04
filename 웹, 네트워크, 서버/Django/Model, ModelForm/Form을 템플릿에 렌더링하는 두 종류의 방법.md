---
created : 2023-04-03, Mon
topics : Form을 템플릿에 렌더링하는 두 종류의 방법
context : django, python
tags: python/django/template_language
---
# Form을 템플릿에 렌더링하는 두 종류의 방법
## [Form rendering options](https://docs.djangoproject.com/en/3.2/topics/forms/#form-rendering-options)

There are other output options though for the `<label>`/`<input>` pairs:

- `{{ form.as_table }}` will render them as table cells wrapped in `<tr>` tags
- `{{ form.as_p }}` will render them wrapped in `<p>` tags
- `{{ form.as_ul }}` will render them wrapped in `<li>` tags

Note that you’ll have to provide the surrounding `<table>` or `<ul>` elements yourself.

## [Rendering fields manually](https://docs.djangoproject.com/en/3.2/topics/forms/#rendering-fields-manually)

> [[Form Field 속성, 메서드]] 참조. [[Widgets 사용법, 예시, 필드 클래스#^0dce50]]도 참조하라.  
> django의 [[Filter, Tag, Variable|template language]]를 사용해 폼의 필드를 폼의 속성처럼 사용할 수 있음. `{{ form.name_of_field }}`와 같이 사용한다. (어떤 속성들이 available한지 어떻게 알 수 있지?)

