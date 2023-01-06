다음은 [백준 25304번 문제](https://www.acmicpc.net/problem/25304)에 대한 숏코딩이다
```python
X,N,*A=open(0)
print("YNeos"[int(X)!=sum(eval(i.replace(*' *'))for i in A)::2])
```
이 코드는 메모리 30840KB를 차지하고, 72ms가 걸린다.  
아래는 내가 제출한 코드이다
```python
n = list(map(int, open(0).read().split()))
nn = n[2:]

total = 0
l = int(len(nn)/2)
for i in range(l):
    total += (nn[i*2] * nn[i*2+1])

if total == n[0]:
    print('Yes')
else:
    print('No')
```
길이는 숏코딩보다 훨씬 길다. 메모리 사용도 30616KB로 비슷하지만, 시간 36ms를 소요하여 위 코드보다 2배정도 빠르다.

# 결론
짧은 코드가 항상 좋은 것은 아니다.