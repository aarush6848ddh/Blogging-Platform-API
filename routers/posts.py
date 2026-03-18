from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db
import redis
import json

r = redis.Redis(host='redis', port=6379, decode_responses=True)

# This router handles all the endpoints related to blog posts.
router = APIRouter(prefix="/posts", tags=["Posts"])

# This endpoint creates a new post. 
# It expects a PostCreate schema in the request body 
# and returns a PostResponse schema with the created 
# post's data. The status code 201 indicates that a 
# new resource has been successfully created.
@router.post("/", response_model=schemas.PostResponse, status_code=201)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)

# This endpoint retrieves a list of posts.
# It accepts an optional search query parameter to filter posts by title.
# It returns a list of PostResponse schemas matching the search criteria.
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(search: str = "", db: Session = Depends(get_db)):
    return crud.get_posts(db, search)

# This endpoint retrieves a single post by its ID.
# If the post with the given ID does not exist, it raises a 404 error.
@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    cache_key = f"post:{post_id}" # Generate a unique cache key for the post based on its ID
    cached = r.get(cache_key) # Check if the post data is already cached in Redis. If it is, return the cached data as a JSON object. If not, retrieve the post from the database, cache it in Redis for future requests, and then return the post data. This caching mechanism helps to reduce database load and improve response times for frequently accessed posts.
    if cached:
        return json.loads(cached)
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    r.setex(cache_key, 60, schemas.PostResponse.model_validate(post).model_dump_json()) # Cache the post data in Redis with an expiration time of 60 seconds (1 minute)
    return post

# This endpoint updates an existing post by its ID.
# It accepts a PostUpdate schema in the request body, 
# which allows for partial updates.
# If the post with the given ID does not exist, it raises a 404 error.
@router.patch("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db, post_id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

# This endpoint deletes a post by its ID.
# If the post with the given ID does not exist, it raises a 404 error.
# The status code 204 indicates that the request was successful but there 
# is no content to return as we have deleted the resource. 
# This is a common status code for successful delete operations.
@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted_post = crud.delete_post(db, post_id)
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")