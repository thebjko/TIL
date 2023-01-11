T = int(input())

for i in range(1, T+1):
    inp = input().split()
    m = map(int, inp)
    max_num = max(*m)
    print(f'#{i} {max_num}')
