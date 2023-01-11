T = int(input())

for i in range(1, T+1):
    ls = list(map(int, input().split()))
    print(f'#{i} {round(sum(ls)/len(ls), 0):.0f}')
