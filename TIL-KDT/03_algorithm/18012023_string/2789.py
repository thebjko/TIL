# 유학 금지
(ls := list('CAMBRIDGE')).sort()
n = list(input().upper())
for i in n:
    if i not in ls:
        print(i, end='')