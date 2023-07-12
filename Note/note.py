from logger import logger
from fastapi import APIRouter, Request, Depends, status, Security
from sqlalchemy.orm import Session
from .model import get_db
from .model import Note
from . import schema
from fastapi.security import APIKeyHeader
from .utils import check_user

note_router = APIRouter(dependencies=[Security(APIKeyHeader(name='Authorization', auto_error=False)),
                                      Depends(check_user)])


@note_router.post('/create_note', status_code=status.HTTP_201_CREATED)
def create_note(request: Request, data: schema.NoteSchema, db: Session = Depends(get_db)):
    try:
        data = data.dict()
        data.update({'user_id': request.state.user.get('id')})
        note = Note(**data)
        db.add(note)
        db.commit()
        db.refresh(note)
        return {'message': 'note created', 'status': 200, 'data': note}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.get('/get_note', status_code=status.HTTP_200_OK)
def get_note(request: Request, db: Session = Depends(get_db)):
    try:
        notes = db.query(Note).filter_by(user_id=request.state.user.get('id')).all()
        print(notes)
        if not notes:
            raise Exception('No notes found for the user')
        data = [note.to_json() for note in notes]
        return {'message': 'User notes', 'status': 200, 'data': data}
    except Exception as e:
        logger.exception(str(e))
        return {'message': str(e), 'status': 400, 'data': {}}


@note_router.put('/update_note/{note_id}', status_code=status.HTTP_200_OK)
def update_note(request: Request, note_id: int, data: schema.NoteSchema, db: Session = Depends(get_db)):
    try:
        data = data.dict()
        data.update({'user_id': request.state.user.get('id')})
        note = db.query(Note).filter_by(id=note_id, user_id=request.state.user.get('id')).one_or_none()
        if not note:
            raise Exception('Note not found')
        [setattr(note, k, v) for k, v in data.items()]
        db.commit()
        db.refresh(note)
        return {'message': 'Note updated', 'status': 200, 'data': note}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.delete('/delete_note/{note_id}', status_code=status.HTTP_200_OK)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=note_id).first()
        if not note:
            raise Exception('Note not found')

        db.delete(note)
        db.commit()

        return {'message': 'Note deleted', 'status': 200}
    except Exception as e:
        logger.exception(str(e))
        return {'message': str(e), 'status': 400}
