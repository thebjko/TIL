# 제로
_, *calls = map(int, open(0).read().split())
stack = []

for call in calls:
    if call != 0:
        stack.append(call)
    else:
        stack.pop()

print(sum(stack))