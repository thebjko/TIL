# 네 수
# A와 B를 붙인 수와 C와 D를 붙인 수의 합
# https://www.acmicpc.net/problem/10824

a, b, c, d = input().split()
print(sum([int(a + b), int(c + d)])) 