from moon import moon

moon = moon().split()

n = 0
for i in moon[0]:
    if i == moon[1]:
        n += 1

print(n)