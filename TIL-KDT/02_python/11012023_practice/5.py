import sys

sys.stdin = open('input_5.txt', 'r')

T = int(input())

for i in range(T):
    n = int(input())
    for j in range(n):
        print(' '.join(input().split()))
        