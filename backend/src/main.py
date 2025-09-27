from fastapi import FastAPI
from routes.posts import router as posts_router

app = FastAPI()

app.include_router(posts_router, prefix='/api/posts', tags=['users'])

@app.get('/')
def root():
    return {
        'Hello': 'World'
    }
