import sys

sys.stdin = open('input_8.txt', 'r')

a, b = map(int, input().split())

for _ in range(a*b):
    print(*map(int, input().split()))
