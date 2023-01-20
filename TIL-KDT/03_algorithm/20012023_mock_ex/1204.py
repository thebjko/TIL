# 최빈수 구하기
import sys
from collections import Counter

sys.stdin = open('input_1204.txt')

for i in range(int(input())):
    n = input()
    ls = input().split()
    counter = dict(Counter(ls))
    print(f"#{n} {[*sorted(counter, key=counter.get, reverse=True)][0]}")

# 딕셔너리 key로 정렬하는 방법 정리