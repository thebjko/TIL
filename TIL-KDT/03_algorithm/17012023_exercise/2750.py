# 수 정렬하기
# N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.
# https://www.acmicpc.net/problem/2750

# input()
print(*sorted([i for i in map(int, open(0).read().split()[1:])]), sep='\n')
