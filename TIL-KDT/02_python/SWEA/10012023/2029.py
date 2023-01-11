# ls = list(map(int, open(0).read().split()))

# for i, j in enumerate(zip(ls[1::2], ls[2::2])):
#     a, b = j
#     c, d = divmod(a, b)
#     print(f'#{i+1} {c} {d}')

T = int(input())

for t in range(1, T+1):
    a, b = list(map(int, input().split()))
    print(f'#{t} {a//b} {a%b}')
