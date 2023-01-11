# 대각선 출력하기
s = [*'+++++']

for i in range(5):
    t = s.copy()
    t[i] = '#'
    print(''.join(t))
    