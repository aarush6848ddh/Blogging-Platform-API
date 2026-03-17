import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# this line retrieves the database URL from an environment variable named DATABASE_URL. 
# If the environment variable is not set, it defaults to a PostgreSQL connection string 
# that points to a database named "blogdb" running on a host named "db" with the username 
# "postgres" and password "password". This allows us to easily configure the database 
# connection without hardcoding sensitive information in our code, and it also makes 
# it easier to switch between different databases (e.g., for development and production) 
# by simply changing the environment variable.

DATABASE_URL = os.getenv("DATABASE_URL",
  "postgresql://postgres:password@db:5432/blogdb")   

# Create the SQLAlchemy engine, which is responsible for managing the connection to the database.
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class that will be used to create database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)            

# Create a base class for our models to inherit from. This is used by SQLAlchemy to define the structure of our database tables.                                                                                        
Base = declarative_base()

# Dependency function to get a database session. This will be used in our API endpoints to interact with the database.
def get_db():                                                                          
      db = SessionLocal() # Create a new database session                                                 
      try:                                                                               
          yield db # Hand the session to the route that needs it                                                                      
      finally:                                                                           
          db.close() # always close the session after we're done with it to free up resources