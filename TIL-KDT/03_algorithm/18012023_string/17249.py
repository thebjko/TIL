# 태보태보 총난타
s = input()
l = s[:s.index("(")]
r = s[s.index(")"):]
print(l.count("@="), r.count("=@"))