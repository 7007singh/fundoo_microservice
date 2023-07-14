from sqlalchemy import create_engine, Column, String, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get('LABEL_DB'))

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class Label(Base):
    __tablename__ = 'label'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50))
    user_id = Column(BigInteger, nullable=False)

    def to_json(self):
        return {'id': self.id, 'name':  self.name}


class NoteLabelAssociation(Base):
    __tablename__ = 'label_association'

    id = Column(BigInteger, primary_key=True, index=True)
    label_id = Column(BigInteger, nullable=False)
    note_id = Column(BigInteger, nullable=False)
