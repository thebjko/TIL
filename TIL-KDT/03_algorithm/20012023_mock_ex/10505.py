# 소득 불균형

import sys
from math import ceil

sys.stdin = open("input_10505.txt")

T = int(input())

for i in range(T):
    n = int(input())
    ls = list(map(int, input().split()))
    average = sum(ls) / n
    ls = list(map(lambda x: x <= average, ls))

    print(f"#{i + 1} {sum(ls)}")
