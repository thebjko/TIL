import sys

sys.stdin = open('input_2.txt', 'r')

print(' '.join(sys.stdin.read().split()))