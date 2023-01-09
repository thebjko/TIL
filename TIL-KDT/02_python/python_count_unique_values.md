[Python: Count Unique Values in a List (4 Ways) • datagy](https://datagy.io/python-count-unique-values-list/)

# Counter 클래스 사용
```python
# Use Counter from collections to count unique values in a Python list
from collections import Counter 

a_list = ['apple', 'orage', 'apple', 'banana', 'apple', 'apple', 'orange', 'grape', 'grape', 'apple'] 

counter_object = Counter(a_list) 
keys = counter_object.keys() 
num_values = len(keys) 

print(num_values)   # Returns 5
```

# numpy 라이브러리의 `.unique()` 메서드 사용
```python
# Use numpy in Python to count unique values in a list 
import numpy as np 

a_list = ['apple', 'orage', 'apple', 'banana', 'apple', 'apple', 'orange', 'grape', 'grape', 'apple'] 

array = np.array(a_list) 
unique = np.unique(array) 
num_values = len(unique) 

print(num_values)
```

# for-loop 및 `set()`
생략