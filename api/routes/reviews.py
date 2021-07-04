from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import User
from ..database import Movie
from ..database import UserReview

from ..schemas import ReviewRequestModel
from ..schemas import ReviewRequestPutModel
from ..schemas import ReviewResponseModel

router = APIRouter(prefix='/reviews')

@router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=400, detail='User not found.')
    
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='Movie not found.')

    user_review = UserReview.create(
        user_id = user_review.user_id,
        movie_id = user_review.movie_id,
        review = user_review.review,
        score = user_review.score
    )

    return user_review


@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)
    
    return [ user_review for user_review in reviews ]

@router.get('/{id}', response_model=ReviewResponseModel)
async def get_review(id: int):
    user_review = UserReview.select().where(UserReview.id == id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not fond.')

    return user_review


@router.put('/{id}', response_model=ReviewResponseModel)
async def update_review(id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not fond.')

    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review


@router.delete('/{id}', response_model=ReviewResponseModel)
async def delete_review(id: int):
    user_review = UserReview.select().where(UserReview.id == id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review not fond.')

    user_review.delete_instance()

    return user_review