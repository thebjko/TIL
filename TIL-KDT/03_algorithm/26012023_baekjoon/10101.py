# 삼각형 외우기

a, b, c = angles = sorted(map(int, open(0)))

if sum(angles) != 180:
    print("Error")
else:
    if a == b == c == a:
        print("Equilateral")
    elif a == b or b == c:
        print("Isosceles")
    else:
        print("Scalene")


