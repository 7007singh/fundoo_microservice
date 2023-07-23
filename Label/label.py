from logger import logger
from fastapi import Request, Depends, APIRouter, Security, status
from . import schema
from .model import Session, get_db, Label, NoteLabelAssociation
from fastapi.security import APIKeyHeader
from .utils import check_user, fetch_note

label_router = APIRouter(dependencies=[Security(APIKeyHeader(name='Authorization', auto_error=False)),
                                       Depends(check_user)])


@label_router.post('/add_label', status_code=status.HTTP_201_CREATED)
def create_label(request: Request, data: schema.LabelSchema, db: Session = Depends(get_db)):
    try:
        data = data.model_dump()
        data.update({'user_id': request.state.user.get('id')})
        label = Label(**data)
        db.add(label)
        db.commit()
        db.refresh(label)
        return {'message': 'label added', 'status': 201, 'data': label}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.get('/get_label', status_code=status.HTTP_200_OK)
def get_label(request: Request, db: Session = Depends(get_db)):
    try:
        label = db.query(Label).filter_by(user_id=request.state.user.get('id')).all()
        print(label)
        return {'message': 'labeled notes', 'status': 200, 'data': label}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.put('/update_label/{label_id}', status_code=status.HTTP_200_OK)
def update_label(request: Request, label_id: int, data: schema.LabelSchema, db: Session = Depends(get_db)):
    try:
        data = data.model_dump()
        label = db.query(Label).filter_by(id=label_id, user_id=request.state.user.get('id')).one_or_none()
        if not label:
            raise Exception('label not found')
        [setattr(label, k, v) for k, v in data.items()]
        db.commit()
        db.refresh(label)
        return {'message': 'Note updated', 'status': 200, 'data': label}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.delete('/delete_label/{label_id}', status_code=status.HTTP_200_OK)
def delete_label(request: Request, label_id: int, db: Session = Depends(get_db)):
    try:
        label = db.query(Label).filter_by(id=label_id, user_id=request.state.user.get('id')).one_or_none()
        if not label:
            raise Exception('label not found')
        db.delete(label)
        db.commit()
        return {'message': 'label deleted successfully', 'status': 200, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.post('/associate_label', status_code=status.HTTP_200_OK)
def associate_label(request: Request, data: schema.Association, db: Session = Depends(get_db)):
    try:
        note = fetch_note(data.note_id, token=request.headers.get('Authorization'))
        if not note:
            raise Exception(f"Note {data.note_id} not found")

        associations = []
        for i in data.label_id:
            label = db.query(Label).filter_by(id=i, user_id=request.state.user.get('id')).one_or_none()
            if not label:
                raise Exception(f"Label {i} not found")
            associations.append(NoteLabelAssociation(label_id=label.id, note_id=note.get('id')))
        db.add_all(associations)
        db.commit()

        return {'message': 'Label associated with notes', 'status': 200}
    except Exception as e:
        logger.exception(str(e))
        return {'message': str(e), 'status': 400}


@label_router.delete('/delete_label_association', status_code=status.HTTP_200_OK)
def delete_label_association(request: Request, data: schema.Association, db: Session = Depends(get_db)):
    try:
        note = fetch_note(data.note_id, token=request.headers.get('Authorization'))
        if not note:
            raise Exception(f"Note {data.note_id} not found")
        for i in data.label_id:
            label = db.query(Label).filter_by(id=i, user_id=request.state.user.get('id')).one_or_none()
            if not label:
                raise Exception(f"Label {i} not found")
            association = db.query(NoteLabelAssociation).filter_by(note_id=data.note_id,
                                                                   label_id=label.id).one_or_none()
            db.delete(association)
        db.commit()
        return {'message': 'Association removed', 'status': 200, 'data': {}}
    except Exception as e:
        logger.exception(str(e))
        return {'message': str(e), 'status': 400}
