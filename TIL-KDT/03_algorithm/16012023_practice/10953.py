# 두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.
# re 라이브러리 사용해 delimiter 여러개로 split하기
# https://datagy.io/python-split-string-multiple-delimiters/
import re

input_string = open(0).read().strip()
split_string = re.split(r',|\n', input_string)
ls = list(map(int, split_string))
a = list(zip(ls[1::2], ls[2::2]))
print(*map(sum, a), sep='\n')