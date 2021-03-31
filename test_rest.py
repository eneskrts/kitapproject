import requests
from pprint import pprint

def client():
    #{'key': '23bfb3260b727501b2204723f570880a68484e2e'}
    token = 'Token 23bfb3260b727501b2204723f570880a68484e2e'
    credentials = {
        'username':'eneskaratas@gmail.com',
        'password':'Samsung799@'
    }
    headers = {
        'Authorization' : token
    }
    response = requests.get(
        url ="http://127.0.0.1:8001/kullanici/api/test",
        headers = headers
    )
    print("statıts",response.status_code)
    response_data = response.json()
    pprint(response_data)


if __name__ == "__main__":
    client()