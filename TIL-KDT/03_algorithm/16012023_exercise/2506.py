# 점수계산

_, *a = list(open(0).read().split())
n = 0
inc = 1
for i in a:
    if i == '1':
        n += inc
        inc += 1
    else:
        inc = 1

print(n)

"""
숏코딩 분석
Originally:
print(sum([p:=int(x)*(p+1)for x in[*open(0)][1].split()]))

Equivalently (in functionality):
ls = []
for x in [*open(0)][1].split():
    ls.append(p := int(x) * (p + 1))
    
print(sum(ls))
"""