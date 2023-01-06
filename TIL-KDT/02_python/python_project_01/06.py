import json
from pprint import pprint
from operator import itemgetter as ig

# 아래 코드 수정 금지
movies_json = open("data/movies.json", encoding="UTF8")
movies_list = json.load(movies_json)

# 이하 문제 해결을 위한 코드 작성
print(type(movies_list))

result = []
keys = ['id', 'title', 'vote_average', 'overview', 'genre_ids', 'poster_path']

for movie in movies_list:
    result.append(dict(zip(keys, ig(*keys)(movie))))

pprint(result, sort_dicts=False)

movies_json.close()