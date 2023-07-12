from pydantic import BaseModel
from typing import Optional, List


class NoteSchema(BaseModel):
    title: str
    description: str
    color: str


class CollaboratorSchema(BaseModel):
    note_id: int
    user_id: Optional[List[int]]
