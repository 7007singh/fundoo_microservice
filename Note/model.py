from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get('NOTE_DB'))

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(200))
    color = Column(String(30))
    user_id = Column(BigInteger, nullable=False)

    def to_json(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'color': self.color,
                'user_id': self.user_id}


class Collaborator(Base):
    __tablename__ = 'collaborator'

    id = Column(BigInteger, primary_key=True, index=True)
    note_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)



