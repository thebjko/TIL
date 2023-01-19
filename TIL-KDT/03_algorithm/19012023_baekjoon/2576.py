# 홀수

n = map(int, open(0).read().split())
ls = [i for i in n if i % 2 == 1]
if ls:
    print(sum(ls), min(ls), sep="\n")
else:
    print(-1)