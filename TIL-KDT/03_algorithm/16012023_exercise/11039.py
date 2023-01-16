for a in (l := list(map(int, open(0).read().split()))):
    if a < 40:
        l[l.index(a)] = 40

print(sum(l)//len(l))