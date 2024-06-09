from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

contacts = []

class Contact(BaseModel):
    id: Optional[UUID] = None
    number: str
    name: Optional[str] = None

@app.post('/add-phone-number/', response_model=Contact)
def create_contact(contact: Contact):
    contact.id = uuid4()
    contacts.append(contact)
    return contact

@app.get('/contacts/', response_model=List[Contact])
def get_contacts():
    return contacts

@app.get('/contact/{contact_id}', response_model=Contact)
def get_contact(contact_id: UUID):
    for contact in contacts:
        if contact.id == contact_id:
            return contact
    raise HTTPException(status_code=404, detail='Contact not found')

@app.put('/update_contacts/{contact_id}', response_model=Contact)
def update_contact(contact_id: UUID, contact_update: Contact):
    for idx, contact in enumerate(contacts):
        if contact.id == contact_id:
            updated_contact = contact.copy(update=contact_update.dict(exclude_unset=True))
            contacts[idx] = updated_contact
            return updated_contact
    raise HTTPException(status_code=404, detail='Contact not found')

@app.delete('/delete_contact/{contact_id}', response_model=Contact)
def delete_contact(contact_id: UUID):
    for idx, contact in enumerate(contacts):
        if contact.id == contact_id:
            return contacts.pop(idx)
    raise HTTPException(status_code=404, detail='Contact not found')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)