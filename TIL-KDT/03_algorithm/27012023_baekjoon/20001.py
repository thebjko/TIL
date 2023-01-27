input()
stack = []
while True:
    q = input()
    if q == "문제":
        stack += [q]
    elif q == "고무오리":
        try:
            stack.pop()
        except IndexError:
            stack += ["문제", "문제"]
    else:
        break

if stack:
    print("힝구")
else:
    print("고무오리야 사랑해")