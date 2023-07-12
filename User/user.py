from logger import logger
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from .model import get_db, User
from . import schema
from passlib.hash import pbkdf2_sha256
from User.utils import JWT


user_router = APIRouter()


@user_router.post('register', status_code=status.HTTP_201_CREATED)
def register_user(data: schema.User, db: Session = Depends(get_db)):
    try:
        data = data.dict()
        data['password'] = pbkdf2_sha256.hash(data['password'])
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": 'User registered successfully', 'Status': 201, 'data': user}
    except Exception as e:
        logger.exception(e.args[0])
        return {"message": e.args[0], 'Status': 400, 'data': {}}


@user_router.post('login', status_code=status.HTTP_200_OK)
def login_user(response: Response, login: schema.Login, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(username=login.username).one_or_none()
        if user and pbkdf2_sha256.verify(login.password, user.password):
            token = JWT.jwt_encode({'user': user.id})
            return {"message": 'Logged in successfully', 'status': 200, 'access_token': token}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": 'Invalid username or password', 'status': 400, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = 400
        return {"message": e.args[0], 'status': 400, 'data': {}}


@user_router.get('/authenticate', status_code=status.HTTP_200_OK)
def authenticate(response: Response, token: str, db: Session = Depends(get_db)):
    try:
        payload = JWT.jwt_decode(token=token)
        user = db.query(User).filter_by(id=payload.get('user')).one_or_none()
        return user.to_json()
    except Exception as e:
        response.status_code = 401
        return {'message': str(e)}
