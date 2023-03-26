Tim_Berners_Lee.html 중 일부:
```html
<img class="picture" src="https://hg-edu.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fe6ff5491-22ad-4bbf-b973-90adaadec36f%2F01_HTML_CSS_Basics_01_01.jpg?id=21ff0c8b-b1ac-4661-a3b4-9f25d321573a&table=block&spaceId=f7ab64f0-6613-4035-b609-06b6865d9b61&width=600&userId=&cache=v2" alt="팀 버너스리">
```
style.css:
```css
.picture {
  margin: auto;
  width: 80%;
  max-height: auto;
  display: block;
}
```

`img` 태그를 가운데 정렬하면서 크기가 창 크기, 좀 더 정확히는 부모 엘리먼트의 크기에 따라 조절되도록 하려고 한다.
1. `margin: auto;` : 좌 우 margin의 크기를 맞춘다. picture 클래스를 속성으로 가진 img 태그를 가운데 정렬시키는데 핵심이다.
2. `width: 80%;` : 이미지 태그의 너비를 조절한다. 부모 태그 너비의 80%를 차지하게 값이 선언되어 있다.
3. `max-height: auto;`와 같이 이미지의 전체 크기를 조절하는데 부모 태그 너비가 변하면서 이미지 태그의 너비도 변할 때 최대 크기 또한 유동적으로 늘어나게 되어있다.
	- 만약 여기서 `width` 속성에 고정된 값을 주면 가운데 정렬은 유지되지만 부모 요소의 너비가 넓어짐에 따라 변하지 않게 된다.
	- `max-height` 속성에 고정된 값을 주면 그 값 까지만 높이가 커지고 더 늘리면 이미지 비율이 깨지게 된다. `max-height`까지 도달하면 `width`도 늘어나지 않게 할 수 없을까?
4. `display: block;` : 이 선언을 하지 않으면 `img` 태그의 박스 타입이 디폴트 값인 `inline`이 되어 `margin` 속성에 `auto`값이 적용되지 않게 된다.

# 도전과제
1. `max-height` 고정된 값으로 지정하면서 도달했을 때 `width`도 증가하지 않도록 하는 방법 알아보기
	- `max-width` 속성에 고정된 값을 선언함으로 해결했다.
	- 여기까지는 `display: block;` 없이도 가능하다.
```css
.picture {
  margin: auto;
  width: 80%;
  max-width: 500px;
  max-height: auto;
  display: block;
}
```

2. 박스 타입 변경하지 않고 가운데 정렬하기
	- `display: inline-block;` 으로는 해결되지 않는다.
	- `img` 태그를 `div` 태그로 감싸고 `picture` 클래스 속성을 `div`에 할당하면 가운데 정렬이 되긴 하지만 크기가 저절로 조절되지 않는다.
	- `img` 크기가 고정되고 `div`는 거기에 맞추기 때문인 것 같다.
	- `block` 타입과 `inline` 타입의 디폴트 크기는 자식 요소에 맞춰 결정된다. 하지만 `block` 타입은 너비를 제한하더라도 옆에 다른 요소가 올 수 없는 반면 `inline` 타입은 높이, 너비를 지정할 수 없는 대신 옆에 다른 요소가 올 수 있다.
	- 두 가지의 기능들을 `inline-block` 타입을 선언해 사용할 수 있다. `inline-block` 타입은 좌우 끝까지 차지하지 않으면서 높이와 너비를 지정할 수 있다. '인라인이지만 블락처럼' 쓸 수 있다.
	- `div` 태그는 디폴트가 block이다
	- 그렇다면 사이즈는 이미지태그에 주고 마진은 `div`에 주면 될까?
	- 되긴 되는데 `margin: auto;`가 아니라 `text-align: center;`를 통해 가운데 정렬할 수 있었다. 크기도 잘 조절된다.
	- **해결!**

## 결과:
```css
.picture {
  width: 80%;
  max-width: 500px;
  max-height: auto;
}
 
.container {
  text-align: center;
}
```

# 더 생각해 볼 주제 : `margin: auto;`
> The browser selects a suitable margin to use. For example, in certain cases this value can be used to center an element. - MDN

MDN에서는 적절한 `margin`을 브라우저가 결정한다고 한다. `img`의 `auto`는 가운데 정렬로 결정되는 반면 왜 `div`에서는 되지 않는걸까?