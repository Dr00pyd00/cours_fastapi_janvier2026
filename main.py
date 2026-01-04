from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# schema:
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome to my API!"}


@app.get("/posts")
async def get_posts():
    return {"data":"This is your posts."}


@app.post("/create_post")
async def create_post(new_post: Post ):
    print(new_post.model_dump())
    return {"new_post": new_post}
