from fastapi import FastAPI
from fastapi import APIRouter

from .database import database as connection

from .database import User
from .database import Movie
from .database import UserReview

from .routes import  user_router
from .routes import review_router


app = FastAPI(title="Proyecto para reseñar películas",
            description="En este proyecto seremos capaces de receñar películas",
            version="1.0")

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)

app.include_router(api_v1)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
        connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('close...')

@app.get('/')
async def index():
    return 'Hola mundo desde FastAPI'

  
