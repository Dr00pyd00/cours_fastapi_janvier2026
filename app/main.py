from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

# func for retrieve post by id:
def find_post_by_id(id:int):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

# func for have index of a post:
def index_of_post_by_id(id:int):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None


# schema:
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# list for posts:
my_posts = [
    {"title":"T1", "content":"content 1", "id":1 },
    {"title":"T2", "content":"content 2", "id":2 },
    {"title":"T3", "content":"content 3", "id":3 },
    ]


# SQL
try:
    conn = psycopg2.connect(host= "localhost",
                    database= "tutoDB",
                    user= "postgres",
                    password= "kottak",
                    cursor_factory= RealDictCursor,
                    )
    cursor = conn.cursor()
    print("database connected!")

except Exception as e:
    print(f"ERROR db connect: {e}")





# start app
app = FastAPI()

# test root
@app.get("/")
async def root():
    return {"message":"Welcome to my API!"}

###################################################
# CRUD for posts
##################################################

# GET all
@app.get("/posts")
async def get_all_posts():
    return {"data":my_posts}

# CREATE post
@app.post("/posts", status_code= status.HTTP_201_CREATED)
async def create_post(new_post: Post ):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0,10000000)
    my_posts.append(post_dict) 
    return {"new_post": new_post}

# GET latest post
@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) -1]
    return {"latest_post": post }


# GET post by ID
@app.get("/posts/{id}")
def get_post_detail(id:int):
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"the post with ID:{id} NOT FOUND!" 
                )
    return {"post_detail": post } 


# DELETE a post by ID:
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id:int):
    post_to_delete = find_post_by_id(id)
    if not post_to_delete:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"the post with ID:{id} NOT FOUND!" 
                )
    # faire le delete propre:
    my_posts.remove(post_to_delete)
    return
 
# UPDATE a post by id:
@app.put("/posts/{id}", status_code= status.HTTP_201_CREATED )
async def update_post(id: int, new_post_entries:Post):
    post_index = index_of_post_by_id(id)
    if post_index is None:
        raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= f"the post with ID:{id} NOT FOUND!"
                )
    # change
    post_dict = new_post_entries.model_dump()
    post_dict["id"] = id
    my_posts[post_index] = post_dict

    return {"updated_post": post_dict }







