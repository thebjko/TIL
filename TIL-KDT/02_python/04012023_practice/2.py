ls =list(map(int, input()[1:-1].split(',')))

n = 0
while True:
    try:
        ls[n]
    except IndexError:
        print(n)
        break
    else:
        n += 1

# 또는
for _ in ls:
    n += 1

print(n)

