name = input('name? ')
phone_number = input('phone number? ')
place = input('place? ')
info_dict = {
    '이름': name,
    '전화번호': phone_number,
    '거주지': place,
}

print(info_dict)
for i in info_dict.items():
    print(f'{i[0]} : {i[1]}')