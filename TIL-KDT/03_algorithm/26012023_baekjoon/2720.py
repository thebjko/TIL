# 세탁소 사장 동혁
import sys

sys.stdin = open("input_2720.txt")

for i in range(int(input())):
    change = int(input())
    coins = [25, 10, 5, 1]
    changes = []
    for i in coins:
        changes += [change // i]
        change %= i
    print(*changes)
