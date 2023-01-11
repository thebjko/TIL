# 1대 1 가위바위보

a, b = input().split()
# print(a, b)
# print(type(a), type(b))
# print(ord(a), ord(b))

if ord(a) - ord(b) == 2:
    print('B')
elif int(a) - int(b) == -2:   # ord(a) - ord(b) == -2
    print('A')
elif a > b:
    print('A')
elif a < b:
    print('B')