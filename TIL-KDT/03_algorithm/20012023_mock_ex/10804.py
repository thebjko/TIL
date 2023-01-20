# 문자열의 거울상

import sys

sys.stdin = open("input_10804.txt")

T = int(input())

mirror = ["b", "p", "d", "q"]

for i in range(T):
    ls = []
    for j in input():
        ls.append(mirror[(mirror.index(j) + 2) % 4])
    
    print(f"#{i + 1} {''.join(reversed(ls))}")
