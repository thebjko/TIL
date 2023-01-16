# 두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.

ls = list(map(int, open(0).read().split()))
a = list(zip(ls[1::2], ls[2::2]))
print(*map(sum, a), sep='\n')