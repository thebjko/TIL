# 열 개씩 끊어 출력하기

a = input()
for i in range(len(a)//10 + 1):
    print(a[10*i:10*i+10])
