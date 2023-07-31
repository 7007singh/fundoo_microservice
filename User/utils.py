import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.utcnow() + timedelta(hours=2), iat=datetime.utcnow())
        return jwt.encode(payload, os.environ.get('KEY'), algorithm="HS256")

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, os.environ.get('KEY'), algorithms=['HS256'])
        except jwt.PyJWTError as e:
            raise e


