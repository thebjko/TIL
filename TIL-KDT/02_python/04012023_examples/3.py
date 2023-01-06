a, b, c, d = 0, 0, 0, 0
n = 10

for number in range(n):
    if number % 2 == 0:
        a = a + 1
        
    if number % 3 == 0:
        b = b + 1
        
    if number % 4 == 0:
        c = c + 1
        
    if number % 5 == 0:
        d = d + 1

print(a, b, c, d) # 5 4 3 2