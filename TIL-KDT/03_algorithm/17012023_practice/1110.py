# 더하기 사이클
# https://www.acmicpc.net/problem/1110

ls = [int(input())]

for i in ls:
    a = i // 10   
    b = i % 10
    c = a + b
    d = b * 10 + c % 10
    if d == ls[0]:
        print(len(ls))
        break

    ls.append(d)