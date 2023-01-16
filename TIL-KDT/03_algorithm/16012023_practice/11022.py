# 두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.

nums = [*open(0)]
j = 1
for i in nums[1:]:
    a, b = map(int, i.strip().split())
    print(f'Case #{j}: {a} + {b} = {a + b}')
    j += 1