import sys

sys.stdin = open('input_4.txt', 'r')

T = int(input())
for t in range(1, T+1):
    N = int(input())
    for n in range(1, N+1):
        string = list(map(str, input().split()))
        print(*string)
        pass