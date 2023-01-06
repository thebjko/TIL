name = input('name? ')
phone_number = input('phone number? ')
email = input('email? ')
place = input('place? ')
info_dict = {
    name : dict(
        전화번호 = phone_number,
        이메일 = email,
        거주지 = place,
    )
}
print(info_dict)