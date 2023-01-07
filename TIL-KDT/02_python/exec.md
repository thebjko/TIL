# exec() 함수
파이썬 함수를 실행하는 함수
```python
# 단을 입력받아 구구단을 출력하는 코드
a = b = int(input())
exec("print(a, '*', b//a, '=', b); b += a;" * 9)
```
인자로 문자열, 코드 객체를 전달한다.

## Parameters 인자값
- object - 문자열이나 코드 객체를 전달한다
- globals - 딕셔너리
- locals - a mapping object? (주로 딕셔너리)

# Examples
```python
"""exec() with a Multi-line Input Program"""
# get a multi-line program as input
program = input('Enter a program:')
# Enter a program:'a = 5\nb=10\nprint("Sum =", a+b)'

# compile the program in execution mode
b = compile(program, 'something', 'exec')

# execute the program
exec(b)
```
```python
"""Checking Usable code with exec()"""
# import all the methods from math library
# import math 는 안됨.
from math import *

# check the usable methods  
exec('print(dir())')
```
```python
"""함수 제한하기"""
# import methods from the math library
from math import *

# use sqrt() method 
mycode='''a = sqrt(9)
print(a)'''

# empty dictionary (global parameter) to restrict the sqrt() method
exec(mycode, {})
```
```python
"""__builtins__를 None 외에 다른걸로 하면 어떻게 될까?"""
from math import *

# set globals parameter to none
globalsParameter = {'__builtins__' : None}
# 모든 글로벌 빌트인 메서드를 차단함

# set locals parameter to take only print() and dir()
localsParameter = {'print': print, 'dir': dir}

# print the accessible method directory
exec('print(dir())', globalsParameter, localsParameter)
```


# 참조링크
https://www.programiz.com/python-programming/methods/built-in/exec