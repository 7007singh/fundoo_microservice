import jwt
from datetime import datetime, timedelta


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.utcnow() + timedelta(hours=1), iat=datetime.utcnow())
        return jwt.encode(payload, 'key', algorithm="HS256")

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, 'key', algorithms=['HS256'])
        except jwt.PyJWTError as e:
            raise e


