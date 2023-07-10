from logger import logger
from fastapi import APIRouter, Request, Depends, status, Security
from sqlalchemy.orm import Session
from .model import get_db
from .model import Note
from . import schema
from fastapi.security import APIKeyHeader
from .utils import check_user

note_router = APIRouter(dependencies=[Security(APIKeyHeader(name='Authorization', auto_error=False)),
                                      ])


@note_router.post('/create_note', status_code=status.HTTP_201_CREATED)
def create_note(request: Request, data: schema.NoteSchema, db: Session = Depends(get_db)):
    try:
        data = data.dict()
        note = Note(**data)
        db.add(note)
        db.commit()
        db.refresh(note)
        return {'message': 'note created', 'status': 200, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 200, 'data': {}}
