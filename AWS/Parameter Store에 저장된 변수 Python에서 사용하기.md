---
created_at : 2023-05-11, Thu
유효기록일 : 2023-05-11, Thu
topics : 
context : 
tags : aws django parameter_store python boto3
related : 
---
# Parameter Store 사용하기
AWS Systems Manager로 이동 후 
![[Systems Manager 클릭.png]]
왼쪽 탭에서 '파라미터 스토어' 선택
![[파라미터 스토어 클릭.png]]
파라미터 생성 클릭
![[파라미터 생성 클릭.png]]
필요한 정보 입력 후 파라미터 생성 클릭
![[파라미터 생성.png]]

# Parameter Store에 저장된 변수 Python에서 사용하기[^1]
다음은 사장님의 냉장고 프로젝트에서 Parameter Store에 저장된 변수를 불러오기 위해 사용한 코드이다.
```python
import boto3

# AWS SSM 클라이언트 인스턴스 생성
ssm_client = boto3.client("ssm", region_name=os.getenv('REGION_NAME'))

# Parameter Store에 저장되어 있는 변수 가져오기
secret_name = ssm_client.get_parameter(Name='/bossmarket/rds/secret_name', WithDecryption=True).get('Parameter').get('Value')
hostname = ssm_client.get_parameter(Name='/bossmarket/rds/hostname', WithDecryption=True).get('Parameter').get('Value')
db_name = ssm_client.get_parameter(Name='/bossmarket/rds/db_name', WithDecryption=True).get('Parameter').get('Value')
```
AdministratorAccess 권한을 갖는 컴퓨터에서 진행했다. 더 자세한 사항은 [Boto3 공식문서](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#ssm)를 참고.

<br>

---
# 참고자료
- [Boto3 1.26.132 documentation on SSM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#ssm)


[^1]: [ParameterStore에서 parameter 가져오기](https://hands-on.cloud/working-with-parameter-store-in-python/)
