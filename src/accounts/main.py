from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Acount(BaseModel):
    id: Optional[UUID] = None
    name: str
    password: str
    date_of_birth: str
    location: str
    bio: Optional[str] = None

acounts = [] 


@app.get('/', response_model=List[Acount])
def acounts():
    return acounts

@app.get('/acount/{acount_id}', response_model=Acount)
def acount(acount_id):
    for acount in acounts:
        if acount.id == acount_id:
            return acount
        
    raise HTTPException(status_code=404, detail='acount not found')

@app.post('/create-acount/', response_model=Acount)
def create_acount(acount: Acount):
    acount.id = uuid4()
    acounts.append(contact)
    return acount


