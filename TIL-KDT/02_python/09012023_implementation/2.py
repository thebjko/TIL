from moon import moon

moon = moon().split()

result = {}
for i in moon:
    result[i] = result.get(i, 0) + 1

print(result)