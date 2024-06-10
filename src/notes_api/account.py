from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Account(BaseModel):
    userid: int
    username: str
