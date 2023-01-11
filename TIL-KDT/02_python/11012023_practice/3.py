import sys

sys.stdin = open('input_3.txt', 'r')

for i in map(int, sys.stdin.read().split()):
    print(i)