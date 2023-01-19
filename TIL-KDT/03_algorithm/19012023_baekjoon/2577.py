# 숫자의 개수
# https://www.acmicpc.net/problem/2577

from collections import Counter

a, b, c = map(int, open(0).read().split())
counter = Counter(str(a * b * c))

for i in range(10):
    print(counter.get(str(i), 0))