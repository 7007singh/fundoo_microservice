from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get('USER_DB'))

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    username = Column(String(50), unique=True)
    password = Column(String)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    email = Column(String(50))

    def to_json(self):
        return {'id': self.id, 'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name}


