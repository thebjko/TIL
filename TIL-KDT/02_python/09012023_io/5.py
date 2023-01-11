from collections import deque

numbers = list(map(int, input().split()))
queue = deque()

for i in numbers:
    queue.append(i)

while queue:
# for _ in enumerate(numbers):
    print(queue.popleft(), end=' ')

print('')