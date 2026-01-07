from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

# schema:
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

# list for posts:
my_posts = [
    {"title":"T1", "content":"content 1", "id":1 },
    {"title":"T2", "content":"content 2", "id":2 },
    {"title":"T3", "content":"content 3", "id":3 },
    ]

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome to my API!"}

###################################################
# CRUD for posts
##################################################

# GET ALL
@app.get("/posts")
async def get_posts():
    return {"data":my_posts}


@app.post("/posts")
async def create_post(new_post: Post ):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0,10000000)
    my_posts.append(post_dict) 
    return {"new_post": new_post}
