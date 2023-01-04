## open(0).read()
백준에서 봤다. 숏코딩.
무슨뜻인가?

```python
import sys
sys.stdin.read()
```
위와 같은 뜻이라고 한다.  
sys를 import할 필요 없이 바로 input을 받을 수 있게 해주는 함수이다.  

인터랙티브 콘솔에서 사용할 때는 코드를 한번에 다 입력하고 실행 후, 입력값을 전달한 뒤 Ctrl+D를 입력해야 나머지 코드가 실행이 된다. 스크립트를 작성하고 실행할 때도 마찬가지. 백준에서는 그대로 제출하면 된다.

# 참고자료
[글 읽기 - 파이썬 open 함수에서 0 인자는 무슨 의미인가요? (acmicpc.net)](https://www.acmicpc.net/board/view/80013)
[python - Integer File Descriptor "0" in open() - Stack Overflow](https://stackoverflow.com/questions/53898231/integer-file-descriptor-0-in-open)
[TIL #020 – open(0) | Mathspp](https://mathspp.com/blog/til/020)
https://itcrowd2016.tistory.com/81
https://it-neicebee.tistory.com/m/118
