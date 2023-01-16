# 주사위 세개
ls = a, b, c = sorted(map(int, open(0).read().split()))

if a == b == c:
    print(10000 + a * 1000)

elif a == b or b == c or a == c:
    reward = 1000
    for i in ls:
        if ls.count(i) == 2:
            reward += i * 50
    print(reward)

else:
    print(max(ls) * 100)
