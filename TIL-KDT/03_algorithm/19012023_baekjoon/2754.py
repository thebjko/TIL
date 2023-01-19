# 학점계산
# https://www.acmicpc.net/problem/2754

n = input()
ls = ["-", "0", "+"]
try: 
    print(round(-(ord(n[0]) - 68) + .7 + .3 * ls.index(n[1]), 2))
except:
    print("0.0")
