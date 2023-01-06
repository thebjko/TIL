import json
from pprint import pprint

# 아래 코드 수정 금지
movie_json = open("data/movie.json", encoding="UTF8")
movie = json.load(movie_json)

genres_json = open("data/genres.json", encoding="UTF8")
genres_list = json.load(genres_json)

# 이하 문제 해결을 위한 코드 작성 
# print(type(movie), type(genres_list))
# print(movie)
# print(genres_list)

pprint(movie['genre_ids'])
ls = []
for i in genres_list:
    if i['id'] in movie['genre_ids']:
        ls.append(i['name'])

print(ls)

# 또는
ls = [i['name'] for i in genres_list if i['id'] in movie['genre_ids']]
print(ls)

movie_json.close()
genres_json.close()