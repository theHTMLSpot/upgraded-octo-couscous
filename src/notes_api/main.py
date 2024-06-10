from fastapi import FastAPI, HTTPException
import mysql.connector
from note import Note
from account import Account

app = FastAPI()

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',      # Hostname of the MySQL server
    user='theHTMLSpot',    # Username
    password='126431',     # Password
    database='nc_notes'    # Name of the database
)



# Define a route handler for the /users/ endpoint
@app.get("/users/")
async def get_users():
    # Create a cursor object
    cur = conn.cursor()

    # Execute a query to fetch data from the user_table
    cur.execute('SELECT * FROM user_table')

    # Fetch all rows from the executed query
    rows = cur.fetchall()

    # Close the cursor
    cur.close()

    # Transform fetched data into list of dictionaries
    users_data = [{"name": row[0], "id": row[1]} for row in rows]

    # Return the fetched data
    return users_data

@app.get('/account/{account_id}')
def get_user(account_id: int):
    cur = conn.cursor()

    cur.execute('SELECT * FROM user_table WHERE userid = %s', (account_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        return {"userid": row[0], "username": row[1]}
    else:
        raise HTTPException(status_code=404, detail="Account not found")


        

@app.get('/all-notes/')
def get_notes():
    # Create a cursor object
    cur = conn.cursor()

    # Execute a query to fetch data from the note_table
    cur.execute('SELECT * FROM note_table')

    # Fetch all rows from the executed query
    rows = cur.fetchall()

    # Close the cursor
    cur.close()

    # Transform fetched data into list of dictionaries
    notes_data = [{"userid": row[0], "noteid": row[1], "title": row[2], "note": row[3]} for row in rows]

    # Return the fetched data
    return notes_data

@app.get('/get-user-notes/{user_id}')
def get_user_notes(user_id):
    # Create a cursor object
    cur = conn.cursor()

    # Execute a query to fetch data from the note_table
    cur.execute('SELECT * FROM note_table')

    # Fetch all rows from the executed query
    rows = cur.fetchall()

    # Close the cursor
    cur.close()

    # Initialize an empty list to store user notes
    user_notes = []

    # Iterate through all rows
    for row in rows:
        # Check if the first column (presumably 'userid') matches the provided user_id
        if row[0] == user_id:
            # Append the row to user_notes if it belongs to the user
            user_notes.append(row)

    # Return the user notes
    return user_notes

@app.get('/user-note/{user_id}/{note_id}')
def get_user_note(user_id, note_id):
    cur = conn.cursor()

    # Execute a query to fetch data from the note_table
    cur.execute('SELECT * FROM note_table WHERE userid =%s AND noteid = %s', (user_id , note_id))
    row = cur.fetchone()
    cur.close()

    if row:
        return {"userid": row[0], "noteid": row[1], "title": row[2], "note": row[3]}
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
    


@app.post('/new_account/', response_model=Account)
def create_account(account: Account):
    cur = conn.cursor()

    # Check if the userid exists in the user_table
    cur.execute('SELECT * FROM user_table WHERE userid = %s', (account.userid,))
    user_exists = cur.fetchone()

    if not user_exists:
        # Insert the new account into user_table
        cur.execute('INSERT INTO user_table (userid, username) VALUES (%s, %s)', (account.userid, account.username))

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cur.close()

        # Return the created account as the response
        return account
    else:
        cur.close()
        raise HTTPException(status_code=422, detail='Account ID already in use')
    


@app.post('/new_note/{user}', response_model=Note)
def create_note(note: Note):
    # Create a cursor object
    cur = conn.cursor()

    # Check if the userid exists in the user_table
    cur.execute('SELECT * FROM user_table WHERE userid = %s', (note.userid,))
    user_exists = cur.fetchone()
    

    if not user_exists:
        # If user does not exist, insert into user_table
        cur.execute('INSERT INTO user_table (userid, username) VALUES (%s, %s)', (note.userid, note.title))

    # Insert the new note into note_table
    cur.execute('INSERT INTO note_table (userid, noteid, title, note) VALUES (%s, %s, %s, %s)', (note.userid, note.noteid, note.title, note.note))

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cur.close()

    # Return the created note as the response
    return note
        
@app.put('/update-account/{account_id}', response_model=Account)
def update_account(account_id: int, update_account: Account):
    cur = conn.cursor()

    # Execute an SQL UPDATE statement to update the account
    cur.execute('UPDATE user_table SET username = %s WHERE userid = %s',
                (update_account.username, account_id))

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cur.close()

    # Return the updated account as the response
    return update_account

@app.put('/update_note/{user_id}/{note_id}', response_model=Note)
def update_note(user_id: int, note_id: int, update_note: Note):
    cur = conn.cursor()

    # Execute an SQL UPDATE statement to update the note
    cur.execute(
        'UPDATE note_table SET title = %s, note = %s WHERE userid = %s AND noteid = %s',
        (update_note.title, update_note.note, user_id, note_id)
    )

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cur.close()

    # Return the updated note as the response
    return update_note

@app.delete('/delete-user/{user_id}')
def delete_user(user_id: int):
    cur = conn.cursor()

    cur.execute('DELETE FROM user_table WHERE userid = %s', (user_id,))

    conn.commit()
    cur.close()
    return {"deleted account": user_id}

@app.delete('/delete-note/{user_id}/{note_id}')
def delete_note(user_id: int, note_id: int):
    cur = conn.cursor()

    cur.execute('DELETE FROM note_table WHERE userid = %s AND noteid = %s', (user_id, note_id))

    conn.commit()
    cur.close()
    return {"deleted note": f"{user_id}/{note_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)