import requests, os
from operator import itemgetter
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

def search_movie(title):
    """
    참고:
    https://developers.themoviedb.org/3/getting-started/search-and-query-for-details
    https://developers.themoviedb.org/3/movies/get-movie-recommendations
    """
    BASE_URL = 'https://api.themoviedb.org/3'
    path = '/search/movie'
    params = {    
        'api_key': os.getenv('API_KEY'),
        'query': '+'.join(title.split()),
        'language': 'ko-KR',
        'region': 'KR',
    }
    
    response = requests.get(BASE_URL+path, params=params)
    result = response.json().get('results')
    
    try:
        return result[0].get('id')

    except:
        return None

# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    제목에 해당하는 영화가 있으면 해당 영화의 id 반환
    검색한 결과 영화가 없다면 None을 반환
    """
    print(search_movie('기생충'))
    # 496243
    print(search_movie('그래비티'))
    # 959101
    print(search_movie('검색할 수 없는 영화'))
    # None
