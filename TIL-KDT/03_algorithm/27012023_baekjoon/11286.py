# 절댓값 힙
from heapq import heapify, heappush, heappop

ls = []
for num in [*open("input_11286.txt")][1:]:
    if (num := int(num)):
        heappush(ls, (abs(num), num))
    elif ls:
        print(heappop(ls)[1])
    else:
        print(0)
