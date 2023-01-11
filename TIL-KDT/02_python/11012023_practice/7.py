import sys

sys.stdin = open('input_7.txt', 'r')

T = list(map(int, input().split()))

for i in range(T[0]*T[1]):
    print(*map(int, input().split()))
    