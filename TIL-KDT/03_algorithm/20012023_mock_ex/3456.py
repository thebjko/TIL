# 3456 직사각형 길이 찾기

import sys
from math import sqrt

sys.stdin = open("input_3456.txt")

T = int(input())

for i in range(T):
    ls = list(map(int, input().split()))
    
    a, b = max(ls), min(ls)
    
    ls.remove(a)
    ls.remove(b)

    c = ls[0]

    print(f"#{i + 1} {int(sqrt(a**2 + b**2 - c**2))}")
