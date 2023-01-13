import requests, os

from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
BASE_URL = "https://api.themoviedb.org/3"
path = "/search/movie"
params = {
    'api_key': os.getenv("API_KEY"),
    'language': 'ko-KR',
    'region': 'KR',
}

def get_movie_id(title: str) -> str:
    # global path
    # global params

    params.update(query=title)
    response = requests.get(BASE_URL+path, params=params)
    result = response.json().get("results")

    try:
        movie_id = result[0].get("id")
        return movie_id
    except:
        return IndexError


def credits(title):
    global path    
    global params
     
    try:
        movie_id = get_movie_id(title)
        path = f"/movie/{movie_id}/credits"
        
        params.pop("query")
        params.pop("region")
        
        response = requests.get(BASE_URL+path, params=params)
        result = response.json().get("cast")
        
        return [i['name'] for i in result if i.get("cast_id") < 10]

    except:
        return None


# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    제목에 해당하는 영화가 있으면 해당 영화 id를 통해 영화 상세정보를 검색하여 주연배우 목록(cast)과 스태프(crew) 중 연출진 목록 반환
    영화 검색에 실패할 경우 None을 반환
    """
    pprint(credits('인생은 아름다워'))
    # {'cast': ['Song Kang-ho', 'Lee Sun-kyun', ..., 'Jang Hye-jin'], 'crew': ['Bong Joon-ho', 'Park Hyun-cheol', ..., 'Yoon Young-woo']}
    pprint(credits('검색할 수 없는 영화'))
    # None
