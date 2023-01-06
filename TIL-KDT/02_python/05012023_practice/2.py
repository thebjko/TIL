moeum = 'aeiouAEIOU'

m = input('문자열을 입력하세요 > ')
n = 0

for i in m:
    if i in moeum:
        n += 1

print(n)