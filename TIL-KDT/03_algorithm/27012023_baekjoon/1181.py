# 단어 정렬
from heapq import heapify, heappop
heap = []
for word in open("input_1181.txt"):
    word = word.strip()
    heap += [(len(word), word)]

heap = list(set(heap))
heapify(heap)   # set은 heap으로 만들 수 없다

while heap:
    print(heappop(heap)[1])
