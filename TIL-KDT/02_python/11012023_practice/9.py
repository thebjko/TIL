import sys

sys.stdin = open('input_9.txt', 'r')

a, b = map(int, input().split())
c = a * b

while c:
    print(*map(int, input().split()))
    c -= 1
    