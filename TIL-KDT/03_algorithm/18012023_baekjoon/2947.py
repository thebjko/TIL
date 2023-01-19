# 나무 조각
ls = list(open(0).read().split())

while ls != ['1', '2', '3', '4', '5']:
    for i in range(len(ls) - 1):
        if ls[i] > ls[i + 1]:
            ls[i], ls[i + 1] = ls[i + 1], ls[i]
            print(*ls)
