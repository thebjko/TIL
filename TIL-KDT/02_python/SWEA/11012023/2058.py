# 자릿수 더하기

T = int(input())
n = 0
while T:
    n += T%10
    T = T//10

print(n)