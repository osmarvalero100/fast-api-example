from typing import Any

from pydantic import  BaseModel
from pydantic import validator
from pydantic.utils import GetterDict

from peewee import ModelSelect

# Convierte un objeto de tipo model de Peewee a un dicccionario y poder enviarlo como respuesta la cliente
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

class ResponseModel(BaseModel):

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud del username debe ser entre 3 a 50 carácteres.')

        return username

class UserResponseModel(ResponseModel):
    # Retorna solo estos campos del modelo User
    id: int
    username: str

#-------- Movie ------------

class MovieRequestModel(BaseModel):
    title: str


class MovieResponseModel(ResponseModel):
    id: int
    title: str

# --------- Review -----------

class ReviewRequestModel(BaseModel):
    user_id: int
    movie_id: int
    review: str
    score: int

    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El rango para score es de 1 a 5.')
        
        return score


class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    review: str
    score: int


class ReviewRequestPutModel(BaseModel):
    review: str
    score: int

    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El rango para score es de 1 a 5.')
        
        return score

