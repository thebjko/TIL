# 괄호
import sys
sys.stdin = open("input_9012.txt")
input = sys.stdin.readline

for i in range(int(input())):
    stack = []
    ps = input()
    for i in ps:
        if i == "(":
            stack += ["stack"]
        elif i == ")":
            try:
                stack.pop()
            except IndexError:
                stack += ["NO"]
                break
    
    if stack:
        print("NO")
        continue

    else:
        print("YES")
    

