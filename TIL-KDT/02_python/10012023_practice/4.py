# 2개 이상의 정수를 출력하세요
ls = [*map(int, open(0).read().split())]
for i in ls:
    print(i, end=' ')

print('')