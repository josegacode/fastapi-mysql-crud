from fastapi import FastAPI
from routes.user import user

app = FastAPI()

@app.get('/')
def dead_root():
    return { 'test': 'it works' }

app.include_router(user)
