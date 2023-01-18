# 시험 성적

score = int(input())
grade = ['F', 'D', 'C', 'B', 'A', 'A']
print(grade[max(score//10 - 5, 0)])
