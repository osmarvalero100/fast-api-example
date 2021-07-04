import requests

BASE_URL = 'http://localhost:8000/'
HEADERS = {
    'acept': 'application/json'
}

def create_review():
    URL = BASE_URL+'api/v1/reviews'
    REVIEW = {
        'user_id': 7,
        'movie_id': 1,
        'review': 'Buena película',
        'score': 5
    }

    response = requests.post(URL, json=REVIEW)

    if response.status_code == 200:
        print(f'Review id: {response.json()["id"]}')
    else:
        print(response.content)

def update_review():
    REVIEW_ID = 10
    URL = f'{BASE_URL}api/v1/reviews/{REVIEW_ID}'
    REVIEW = {
        'review': 'Película medio buena',
        'score': 3
    }

    response = requests.put(URL, json=REVIEW)

    if response.status_code == 200:
        print('Reseña actualizada:')
        print(response.json())
    else:
        print(response.content)

def delete_review():
    REVIEW_ID = 10
    URL = f'{BASE_URL}api/v1/reviews/{REVIEW_ID}'

    response = requests.delete(URL)

    if response.status_code == 200:
        print('La reseña fue eliminada.')
    else:
        print(response.content)

def get_reviews():
    QUERY_SET = {
        'page': 1,
        'limit': 5
    }

    URL = BASE_URL+'api/v1/reviews'

    response = requests.get(URL, headers=HEADERS, params=QUERY_SET)

    if response.status_code == 200:
        print(response.content)


def get_user_reviews(cookies):
    URL = f'{BASE_URL}api/v1/users/reviews'

    response = requests.get(URL, cookies=cookies)

    if response.status_code == 200:
        print('Reviews:')
        for review in response.json():
             print(f'> {review["review"]} - {review["score"]}')
    else:
        print(response.content)


def login():
    URL = BASE_URL+'api/v1/users/login'
    USER = {
        'username': 'root',
        'password': 'root'
    }

    response = requests.post(URL, json=USER)

    if response.status_code == 200:
        user_id = response.cookies.get_dict().get('user_id')

        print('Usuario autenticado')
        #print(response.json())

        cookies = { 'user_id': user_id }
        get_user_reviews(cookies)


if __name__ == '__main__':
    #get_reviews()
    #create_review()
    #update_review()
    #delete_review()
    login()