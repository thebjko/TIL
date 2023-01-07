# exec() 함수
파이썬 함수를 실행하는 함수
```python
# 단을 입력받아 구구단을 출력하는 코드
a = b = int(input())
exec("print(a, '*', b//a, '=', b); b += a;" * 9)
```
인자로 문자열, 코드 객체를 전달한다.  

## 언제 사용할까?
상상하기가 아직은 쉽지 않다. 사용자에게 문자열로 명령을 받을 때? 코드 객체란 뭐지?  


# 참조링크
https://www.programiz.com/python-programming/methods/built-in/exec
