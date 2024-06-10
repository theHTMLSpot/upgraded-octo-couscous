from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Note(BaseModel):
    userid: int
    noteid: int
    title: str
    note: str

