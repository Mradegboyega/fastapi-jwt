import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Body
from app.models import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer


# in-memory database to store posts
posts = [
    {
        "id": 1,
        "title": "Tiger Post 🐯",
        "text": "This is the content of the Tiger wild animal.",
    },
    {
        "id": 2,
        "title": "Lion Post 🦁",
        "text": "This is the content of the Lion wild animal.",
    },
    {
        "id": 3,
        "title": "Eagle Post 🦅",
        "text": "This is the content of the Eagle birds.",
    },
    {
        "id": 4,
        "title": "Dog Post 🐶",
        "text": "This is the content of the Dog domestic animal.",
    }
]

# in-memory databaset to store users data
users = []

app = FastAPI()

# handler route for welcome pag
@app.get('/', tags=["test"])
def greet():
    return {"message": "Welcome, user!"}

# User signup handler route
@app.post('/user/signup')
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

# function to validate user login
def validate_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post('/user/login')
def login_user(user: UserLoginSchema = Body(default=None)):
    if validate_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }

# handler route to get all posts
@app.get("/posts", dependencies=[Depends(jwtBearer())])
def get_posts():
    return {"data" : posts}

@app.get("/posts/{id}", dependencies=[Depends(jwtBearer())])
def get_posts_by_id(id: int):
    if id > len(posts):
        raise HTTPException(status_code=404, detail=f"Post with ID {id} doesn't exist")

    for post in posts:
        if post["id"] == id:
            return {"data": post}

# Handler route for authorized user to create post        
@app.post("/posts", dependencies=[Depends(jwtBearer())], response_model=PostSchema)
def create_post(post: PostSchema):
    new_post_data = post.model_dump()
    new_post_data["id"] = len(posts) + 1
    new_post = PostSchema(**new_post_data)
    posts.append(new_post_data)
    return {"data": new_post}


# handler route for authorized user to delete post
@app.delete("/posts/{post_id}", dependencies=[Depends(jwtBearer())], response_model=dict)
def delete_post(post_id: int):
    post_to_delete = next((post for post in posts if post["id"] == post_id), None)

    if not post_to_delete:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")

    # Remove the post from the list
    posts.remove(post_to_delete)

    return {"message": f"Post with ID {post_id} deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
