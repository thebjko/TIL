# 네 번째 점
# 세 점이 주어졌을 때, 축에 평행한 직사각형을 만들기 위해서 필요한 네 번째 점을 찾는 프로그램을 작성하시오.
# https://www.acmicpc.net/problem/3009

ls = list(map(int, open(0).read().split()))
result = []
for i in (x := ls[0::2]):
    if x.count(i) == 1:
        result.append(i)

for i in (y := ls[1::2]):
    if y.count(i) == 1:
        result.append(i)

print(*result)

    