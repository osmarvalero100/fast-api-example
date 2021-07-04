from fastapi import HTTPException
from fastapi import APIRouter

from ..database import Movie
from ..schemas import MovieRequestModel
from ..schemas import MovieResponseModel

router = APIRouter(prefix='/movies')

@router.post('', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(status_code=404, detail=f'La película {movie.title} ya existe.')
    
    movie = Movie.create(
        title = movie.title
    )

    return movie