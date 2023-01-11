import sys
sys.stdin = open('input_1.txt', 'r')

print(' '.join(sys.stdin.read().split()))