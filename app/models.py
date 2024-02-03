from pydantic import BaseModel, Field, EmailStr

# Define a Pydantic model using PostSchema
class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    
    class Config:
        json_schema_extra = {
            "post_demo" : {
                "title" : "title of the content",
                "content" : "stuffs of animals",
            }
        }

# Define a Pydantic model using UserSchema
class UserSchema(BaseModel):
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None) 
    password : str = Field(default=None)

    class Config:
        json_schema_extra = {
            "user_demo": {
                "name": "Bek",
                "email": "contact@adegboyega.com.ng",
                "password": "1234"
            }
        }

# Define a Pydantic model using UserLoginSchema
class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None) 
    password : str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "email": "contact@adegboyega.com.ng",
                "password": "1234"
            }
        }