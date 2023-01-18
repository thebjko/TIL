for i in range(int(input())):
    num, word = input().split()
    for j in word:
        print(int(num) * j, end='')
    print('')