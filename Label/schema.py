from typing import Optional, List
from pydantic import BaseModel


class LabelSchema(BaseModel):
    name: str


class Association(BaseModel):
    note_id: int
    label_id: Optional[List[int]]
