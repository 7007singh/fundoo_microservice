from logger import logger
from fastapi import APIRouter, Request, Depends, status, Security
from sqlalchemy.orm import Session
from .model import get_db
from .model import Note, Collaborator
from . import schema
from fastapi.security import APIKeyHeader
from .utils import check_user, fetch_user

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
        collab = db.query(Collaborator).filter_by(user_id=request.state.user.get('id')).all()
        print(collab)
        note = db.query(Note).filter_by(id=collab.note_id)
        notes = db.query(Note).filter_by(user_id=request.state.user.get('id').all())
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


@note_router.post('/collaborate/', status_code=status.HTTP_200_OK)
def add_collaborator(request: Request, data: schema.CollaboratorSchema, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=data.note_id, user_id=request.state.user.get('id')).one_or_none()
        if not note:
            raise Exception('Note not found')
        collaborator = []
        for i in data.user_id:
            user = fetch_user(i)
            if not user:
                raise Exception(f'User {i} not found')
            collaborator.append(Collaborator(note_id=note.id, user_id=user.get('id')))
        db.delete(collaborator)
        db.commit()
        return {'message': 'collaborated added', 'status': 200}
    except Exception as e:
        logger.exception(str(e))
        return {'message': str(e), 'status': 400}


@note_router.delete('/delete_collaborator/', status_code=status.HTTP_200_OK)
def delete_collaborator(request: Request, data: schema.CollaboratorSchema, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=data.note_id, user_id=request.state.user.get('id')).one_or_none()
        if not note:
            raise Exception('Note not found')
        for i in data.user_id:
            user = fetch_user(i)
            if not user:
                raise Exception(f'User {i} not found')
            collaborator = db.query(Collaborator).filter_by(note_id=note.id, user_id=user.get('id')).one_or_none()
            db.delete(collaborator)
        db.commit()
        return {'message': 'collaborator deleted', 'status': 200}
    except Exception as e:
        logger.exception(str(e))
        return {'message': str(e), 'status': 400}
