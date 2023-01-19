# 다이얼
# https://www.acmicpc.net/problem/5622

ls = [3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,8,9,9,9,10,10,10,10]
alphabet = list(map(chr, range(65, 91)))
n = 0
for i in input():
    n += ls[alphabet.index(i)]

print(n)