import sys
sys.stdin = open('input_5.txt', 'r')

T = int(input())
for t in range(1, T+1):
    N = int(input())
    for n in range(N):
        string = list(map(str, input().split()))
        print(*string)
        pass