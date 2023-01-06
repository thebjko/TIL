import json
from operator import itemgetter as ig
from pprint import pprint

# 아래 코드 수정 금지
movie_json = open("data/movie.json", encoding="UTF8")
movie = json.load(movie_json)
movie_json.close()

genres_json = open("data/genres.json", encoding="UTF8")
genres_list = json.load(genres_json)
genres_json.close()

# 이하 문제 해결을 위한 코드 작성
# pprint(movie)
# pprint(genres_list)

ls = []
ls = [i['name'] for i in genres_list if i['id'] in movie['genre_ids']]
movie['genre_names'] = ls

keys = ['id', 'title', 'vote_average', 'overview', 'genre_names']
result = dict(zip(keys, ig(*keys)(movie)))

pprint(result, sort_dicts=False)