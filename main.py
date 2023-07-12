from fastapi import FastAPI
from User import user
from Note import note

user_app = FastAPI(debug=True, title='User_APIs')
note_app = FastAPI(debug=True, title='Note_APIs')
user_app.include_router(user.user_router, prefix='/user', tags=['User'])
note_app.include_router(note.note_router, prefix='/note', tags=['Note'])
