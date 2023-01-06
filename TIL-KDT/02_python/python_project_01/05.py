"""
How to slice a dictionary:
https://stackoverflow.com/questions/40440373/python-how-to-slice-a-dictionary-based-on-the-values-of-its-keys
"""

import json
from pprint import pprint
from operator import itemgetter as ig

# 아래 코드 수정 금지
movie_json = open("data/movie.json", encoding="UTF8")
movie = json.load(movie_json)

# 이하 문제 해결을 위한 코드 작성
# print(type(movie))
# print(movie.keys())
# pprint(movie)

keys = ['id', 'title', 'vote_average', 'overview', 'genre_ids']

# result = {k: movie[k] for k in keys}
# pprint(result, sort_dicts=False)

## 또는
"""
ig(0,1,2,100,101,102) == lambda d : (d[0], d[1], d[2], d[100], d[101], d[102])
"""
# result = dict(zip(keys, ig(*keys)(movie)))
# pprint(result, sort_dicts=False)
"""
zip() 함수는 여러 개의 순회 가능한(iterable) 객체를 인자로 받고,
각 객체가 담고 있는 원소를 터플의 형태로 차례로 접근할 수 있는 반복자(iterator)를 반환합니다.
"""

## 또는
result = {}
for i in keys:
    result[i] = movie[i]

pprint(result, sort_dicts=False)

movie_json.close()