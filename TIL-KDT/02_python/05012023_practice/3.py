import datetime

dict_variable = {
    "이름": "정우영",
    "생년": "2000",
    "회사": "하이퍼그로스",
}

age = datetime.datetime.now().year - int(dict_variable["생년"]) + 1

print(f'나이 : {age}세')