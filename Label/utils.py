import requests
from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv
load_dotenv()


def check_user(request: Request):
    token = request.headers.get('authorization')
    if not token:
        raise HTTPException(detail='token not found', status_code=401)
    response = requests.get(f'{os.environ.get("BASE_URL")}:{os.environ.get("USER_PORT")}/user/authenticate',
                            params={'token': token})
    if response.status_code >= 400:
        raise HTTPException(detail=response.json().get('message'), status_code=response.status_code)
    request.state.user = response.json()


def fetch_note(note_id: int, token: str):
    response = requests.get(f'{os.environ.get("BASE_URL")}:{os.environ.get("NOTE_PORT")}/note/retrieve_note/',
                            params={'note': note_id}, headers={'Authorization': token})
    if response.status_code >= 400:
        return None
    return response.json()


