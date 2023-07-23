---
created_at : 2023-04-15, Sat
유효기록일 : 2023-07-23, Sun
topics : 
context : 
tags : 
related : 
alias : serialize, 직렬화
---
# Serialize, 직렬화
직렬화(serialization)란 객체를 다른 시스템에서도 사용할 수 있게끔 바이트 형태로 변환하는 것을 말합니다. 일반적으로 네트워크 상에서 데이터를 주고받거나, 데이터를 파일로 저장하거나, 데이터베이스에 저장할 때 사용됩니다.

예를 들어, 파이썬 객체를 직렬화하여 JSON 형태로 변환하면 다른 시스템에서도 해당 JSON 데이터를 이해할 수 있게 됩니다. 이를 통해 객체를 쉽게 전송하거나 저장할 수 있습니다. 반대로, JSON 데이터를 역직렬화하여 파이썬 객체로 변환하면 해당 객체를 다시 사용할 수 있습니다. 이러한 과정을 통해 객체의 지속성(persistence)을 보장할 수 있습니다.

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

---
# 참고자료
- ChatGPT
- https://www.django-rest-framework.org/api-guide/serializers/
- 

[^1]: