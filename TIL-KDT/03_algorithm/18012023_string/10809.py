# 알파벳 찾기
word = input().upper()
alphabet = [*map(chr, range(65, 91))]

for i in alphabet:
    if i in word:
        print(word.index(i), end=' ')
    else:
        print(-1, end=' ')