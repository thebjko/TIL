import sys

sys.stdin = open('input_4.txt', 'r')

T = int(input())

for i in range(T):
    n = int(input())
    for j in range(n):
        # a, b = map(int, input().split())
        # print(a, b)
        print(*map(int, input().split()))
