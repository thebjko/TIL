moon = input('문자열을 입력하세요 > ')

n = 0
count_dict = dict()
for j in moon:
    try:
        count_dict[j] += 1
    except:
        count_dict[j] = 1

for i in count_dict:
    print(i, count_dict[i])

# if key not in my_dict:
#   새로운 키 값 쌍을 넣어라