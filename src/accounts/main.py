from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Account(BaseModel):
    id: Optional[UUID] = None
    name: str
    password: str
    date_of_birth: str
    location: str
    bio: Optional[str] = None

accounts = []

@app.get('/', response_model=List[Account])
def get_accounts():
    return accounts

@app.get('/account/{account_id}', response_model=Account)
def get_account(account_id: UUID):
    for account in accounts:
        if account.id == account_id:
            return account
    raise HTTPException(status_code=404, detail='Account not found')

@app.post('/create-account/', response_model=Account)
def create_account(account: Account):
    account.id = uuid4()
    accounts.append(account)
    return account

@app.put('/update-account/{account_id}', response_model=Account)
def update_account(account_id: UUID, account_update: Account):
    for idx, account in enumerate(accounts):
        if account.id == account_id:
            updated_account = account.copy(update=account_update.dict(exclude_unset=True))
            accounts[idx] = updated_account
            return updated_account
    raise HTTPException(status_code=404, detail='Account not found')

@app.delete('/delete-account/{account_id}', response_model=Account)
def delete_account(account_id: UUID):
    for idx, account in enumerate(accounts):
        if account.id == account_id:
            return accounts.pop(idx)
    raise HTTPException(status_code=404, detail='Account not found')