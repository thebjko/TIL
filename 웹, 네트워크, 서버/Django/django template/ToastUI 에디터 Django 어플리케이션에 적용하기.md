---
created_at : 2023-05-27, Sat
유효기록일 : 2023-05-27, Sat
topics : 
context : 
tags : django js toastui javascript
related : 
---
# ToastUI 에디터 Django 어플리케이션에 적용하기

Velog 처럼 textarea를 꾸밀 순 없을까?

## ToastUI 설치
CDN 사용

base.html
```django
<!DOCTYPE html>
<html lang="ko">
<head>
  ...
  {# ToastUI #}
  <link rel="stylesheet" href="https://uicdn.toast.com/editor/latest/toastui-editor.min.css" />
</head>
<body>
  ...
  
  {# ToastUI #}
  <script src="https://uicdn.toast.com/editor/latest/toastui-editor-all.min.js"></script>
</body>
</html>
```

<br>

## ToastUI 적용
create.html
```django
{% extends 'base.html' %}

{% block content %}
<form id="journal-form" action="{% url 'notes:create' %}" method="post" enctype='multipart/form-data'>
  {% csrf_token %}

  {% with journal_form.title as title %}
  <div class="form-group">
    <label for="{{ title.id_for_label }}">{{ title.label }}</label>
    <input type="{{ title.field.widget.input_type }}" class="form-control" id="" placeholder="{{ title.label }}" name="{{ title.name }}" />
  </div>
  {% endwith %}

  {% with journal_form.content as content %}
  <div class="form-group" style="display: none;">
    <label for="{{ content.id_for_label }}">{{ content.label }}</label>
    <textarea id="{{ content.id_for_label }}" class="form-control" placeholder="{{ content.label }}" name="{{ content.name }}"></textarea>
  </div>
  {% endwith %}
  <div id="editor"></div>
  <div>
    {{ journal_image_form.as_p }}
  </div>
  <button type="submit" class="btn btn-primary">작성하기</button>
</form>
<script>
  document.addEventListener('DOMContentLoaded', (event) => {
    const editorDiv = document.getElementById('editor');
    const editor = new toastui.Editor({
      el: editorDiv,
      height: '500px',
      initialEditType: 'markdown',
      previewStyle: 'vertical',
      initialValue: editorDiv.value,
    })
    const journalForm = document.getElementById('journal-form')
    journalForm.addEventListener('submit', (e) => {
      e.preventDefault()
      const journalFormTextArea = document.querySelector('textarea')
      journalFormTextArea.textContent = editor.getMarkdown()
      journalForm.submit()
    });
  });
</script>
</script>
{% endblock content %}
```
`script` 태그 안을 보자. 현재 create.html에서 해당 스크립트를 실행하고 있고, CDN은 base.html에 있기 때문에 `document`에 이벤트 리스너를 달아 `'DOMContentLoaded'`가 발생하면 해당 코드가 실행되도록 한다. 그렇지 않으면 `toastui`를 찾을 수 없다는 오류가 뜰 것이다. 그리고 그 아래 `new` 키워드 뒤로 ToastUI Editor를 생성한다. 에디터의 `el` 인자로 `editor`라는 id를 가진 div 태그를 선택한다. 이 태그 안에 에디터가 생성된다. 여기까지만 하면 화면에 생성된 에디터가 보일 것이다. 

하지만 이대로라면 작성 후 제출 버튼 클릭시 DB에 내용이 기록되지 않을 것이다. 이 때문에 다른 패키지를 찾아봤었는데, NHN에서 만든 에디터라서 그런지, 활발한 해외 커뮤니티에서는 자료를 찾기 힘들었다. `django-tuieditor`라는 패키지도 있었는데, 문서도 열악했고, 잘 되지 않았다.

그래서 정석적인 방법은 아니지만, JS로 목표 기능을 구현했다. 먼저 `form`을 선택한 뒤 이벤트 리스너를 달아 `'submit'` 이벤트가 발생할 경우 `preventDefault` 한다. 제출이 멈춘 동안 기존 `textarea`를 선택해 `textContent`에 editor에 입력된 마크다운 텍스트를 할당한다. 그리고 `submit` 메서드로 제출한다. 기존 `textarea`의 `style` 속성에 `"display: none;"` 값을 할당하면 UI까지 완성.

<br>

---
# 참고자료
- KDT 최무연 강사님


[^1]: 
