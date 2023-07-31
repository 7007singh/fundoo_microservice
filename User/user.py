from logger import logger
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from .model import get_db, User
from . import schema
from passlib.hash import pbkdf2_sha256
from User.utils import JWT
from tasks import send_mail
import os
from dotenv import load_dotenv

load_dotenv()

user_router = APIRouter()


@user_router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(response: Response, data: schema.User, db: Session = Depends(get_db)):
    """
    param:
        response: HTTP response status code
        data: User data for registration, containing username, email, and password.
        db: Database session to interact with the database
    return:
        dict: Dictionary containing token with message and status
    """
    try:
        data = data.model_dump()
        data['password'] = pbkdf2_sha256.hash(data['password'])
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = JWT.jwt_encode({'user': user.id})
        verify_link = f'{os.environ.get("BASE_URL")}:{os.environ.get("USER_PORT")}/user/verify?token={token}'
        send_mail.delay(user.email, verify_link)
        return {"message": 'User registered successfully', 'Status': 201, 'data': token}
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = 400
        return {"message": e.args[0], 'Status': 400, 'data': {}}


@user_router.post('/login', status_code=status.HTTP_200_OK)
def login_user(response: Response, login: schema.Login, db: Session = Depends(get_db)):
    """
    param:
        response: HTTP response status code.
        login: User login credentials, containing username and password.
        db: Database session to interact with the database.
    return:
        dict: Dictionary containing the message and status
    """
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
    """
    param:
        response: HTTP response status code.
        token: token provided by client for authenticate
        db: Database session to interact with the database.
    return:
        dict: Dictionary containing user data
    """
    try:
        payload = JWT.jwt_decode(token=token)
        user = db.query(User).filter_by(id=payload.get('user')).one_or_none()
        return user.to_json()
    except Exception as e:
        response.status_code = 401
        return {'message': str(e)}


@user_router.get('/retrieve_user/', status_code=status.HTTP_200_OK)
def retrieve_user(response: Response, user: int, db: Session = Depends(get_db)):
    """
    param:
        response: HTTP response status code.
        user: user id to retrieve user data
        db: Database session to interact with the database.
    return:
        dict: Dictionary containing user data
    """
    try:
        user = db.query(User).filter_by(id=user).one_or_none()
        return user.to_json()
    except Exception as e:
        response.status_code = 401
        return {'message': str(e)}


@user_router.get('/verify', status_code=status.HTTP_200_OK)
def to_verify(response: Response, token: str, db: Session = Depends(get_db)):
    """
    param:
        response: HTTP response status code.
        token: Verification token provided by the client for user account verification.
        db: Database session to interact with the database.
    return:
        dict: Dictionary with verification status
    """
    try:
        payload = JWT.jwt_decode(token)
        user = db.query(User).filter_by(id=payload.get('user')).one_or_none()
        if not user:
            raise Exception('user not found')
        user.is_verified = True
        db.commit()
        return {'message': 'user verified successfully', 'status': 200}
    except Exception as e:
        response.status_code = 400
        return {'message': str(e)}
