# 0 = not cute / 1 = cute
# 준희는 자기가 팀에서 귀여움을 담당하고 있다고 생각한다. 하지만 연수가 볼 때 그 의견은 뭔가 좀 잘못된 것 같았다. 그렇기에 설문조사를 하여 준희가 귀여운지 아닌지 알아보기로 했다.

# n,*l=map(int,open(0))
ls = list(map(int, open(0).read().split()))[1:]
m = sum(ls)/len(ls)

#print('Junhee is'+(sum(l)<n/2)*' not','cute!')
if m < .5: 
    print("Junhee is not cute!")
else:
    print("Junhee is cute!")
