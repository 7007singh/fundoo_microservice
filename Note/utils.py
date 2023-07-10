import requests
from fastapi import Request, HTTPException


def check_user(request: Request):
    token = request.headers.get('authorization')
    if not token:
        raise HTTPException(detail='token not found', status_code=401)
    response = requests.get(f'http://127.0.0.1:8001/user/authenticate?{token}')
    print(response.json())
