from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

# Here I am inheriting from Base, which is the declarative base class defined in database.py. This allows SQLAlchemy to understand that this class represents a table in the database.
class Post(Base):
      # This sets the name of the table in the database to "posts". If we didn't specify this, SQLAlchemy would automatically generate a table name based on the class name, which might not be what we want.                                                                      
      __tablename__ = "posts" 
      id = Column(Integer, primary_key=True, index=True) # this defines the "id" column of the table, which is an interger that serves as a primary key meaning it uniquely identifies each record in the table. It is also Indexed for faster lookups.
      title = Column(String(200), nullable=False) # the title of the post, required  
      content = Column(Text, nullable=False) # nullable=False means that this column cannot be left empty when creating a new post. It must have some content.
      category = Column(String(100), nullable=False) # the category of the post, required   
      tags = Column(String(500), default="") # default="" means that if no tags are provided when the post is created, it will default to an empty string instead of being null. This allows us to avoid null values in the database and makes it easier to handle cases where no tags are provided.
      created_at = Column(DateTime(timezone=True), server_default=func.now()) # server_default=func.now() means that when a new post is created, the created_at column will automatically be set to the current date and time on the server. This ensures that we always have a timestamp for when each post was created without needing to manually set it in our code.               
      updated_at = Column(DateTime(timezone=True), onupdate=func.now()) # onupdate=func.now() means that when a post is updated, the updated_at column will automatically be set to the current date and time on the server. This allows us to keep track of when each post was last modified without needing to manually update this field in our code.