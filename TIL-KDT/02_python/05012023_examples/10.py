n = 10
total = 0

for number in range(0, n + 1):
    if number % 2 == 0:
        total += number * 2
        print("짝수", total)
    elif number % 2 == 1:
        total += number + 1 * 3
        print("홀수", total)

print(total) # 135 -> 100