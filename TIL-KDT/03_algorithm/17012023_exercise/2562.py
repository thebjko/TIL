# 최댓값
# https://www.acmicpc.net/problem/2562

ls = list(map(int, open(0).read().split()))
print(m := max(ls), (ls.index(m) + 1), sep='\n')