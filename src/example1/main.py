from fastapi import FastAPI
import random

app = FastAPI()


#you will see this when you go to  / 
@app.get("/")
async def root():
    return {'example': 'this is an example', 'data': 18}

@app.get("/random")
async def get_random():
    rn:int = random.randint(0, 100)
    return {'number': rn, 'limit': 100}
@app.get("/random/{limit}")
async def get_random(limit: int):
    rn:int = random.randint(0, limit)
    return {'number': rn, 'limit': limit}