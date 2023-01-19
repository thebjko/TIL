# 회사에 있는 사람
# https://www.acmicpc.net/problem/7785

"""
employees = {}
for i in range(int(input())):
    name, status = input().split()
    employees[name] = status

(ls := sorted([i for i, j in employees.items() if j == 'enter'])).reverse()
print(*ls, sep="\n")

느리다
"""
# 또는
"""
from collections import OrderedDict

print(OrderedDict(sorted(employees.items(), reverse=True)))
"""

ls = open(0).read().split()[1:]
ls = zip(ls[::2], ls[1::2])
employees = {}
employees.update(ls)
print(*sorted([i for i, j in employees.items() if j == 'enter'], reverse=True))

"""20배 더 빠르다 (168ms)"""