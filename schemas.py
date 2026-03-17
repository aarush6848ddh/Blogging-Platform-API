from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# This schema is used for creating a new post.
# It defines the fields that are required when a
# client sends a request to create a new post.
# The tags field is optional and defaults to an
# empty string if not provided.
class PostCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: str = ""

# This schema is used for updating an existing post.
# All fields are optional, allowing clients to update
# only the fields they want to change. = None means that
# if a field is not provided in the update request,
# it will default to None, indicating that it should not be updated.
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None

# This schema is used for responses when retrieving post data.
# It includes all the fields of a post, including the id,
# created_at, and updated_at timestamps.
# The Config class with from_attributes = True allows Pydantic
# to create an instance of PostResponse from a SQLAlchemy model instance.
# This means that when we retrieve a post from the database using SQLAlchemy,
# we can directly return it as a PostResponse without needing to manually
# convert it to a dictionary or another format. Pydantic will
# automatically read the attributes of the SQLAlchemy model and
# populate the fields of the PostResponse accordingly.
class PostResponse(BaseModel):                                                         
      id: int                                                                            
      title: str                                                                         
      content: str                                                                       
      category: str                                                                      
      tags: str                                                                          
      created_at: datetime                                  
      updated_at: Optional[datetime] = None                                              
                                           
      class Config:                                                                      
          from_attributes = True  