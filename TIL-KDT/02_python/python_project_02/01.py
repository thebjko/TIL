import requests, os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
BASE_URL = "https://api.themoviedb.org/3"
path = "/movie/popular"
# API_KEY = os.getenv("API_KEY")
params = {
    'api_key': os.getenv("API_KEY"),
    'language': 'ko-KR',
    'region': 'KR',
}

def popular_count() -> int:
    response = requests.get(BASE_URL+path, params=params)
    if response.status_code == 200:
        response_body = response.json()
        return len(response_body.get("results"))


# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    popular 영화목록의 개수 반환
    """
    print(popular_count())
    # 20
