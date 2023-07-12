import requests
from fastapi import Request, HTTPException


def check_user(request: Request):
    token = request.headers.get('authorization')
    if not token:
        raise HTTPException(detail='token not found', status_code=401)
    response = requests.get(f'http://127.0.0.1:8001/user/authenticate', params={'token': token})
    if response.status_code >= 400:
        raise HTTPException(detail=response.json().get('message'), status_code=response.status_code)
    request.state.user = response.json()
