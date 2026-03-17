from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# This is the database URL for SQLite.
# "sqlite:///" means we are using SQLite and the database file will be located in the current directory.
# SQLite is a lightweight, file-based database that is easy to set up and use for small applications like this one.
# "./blog.db" specifies the name of the database file. If it doesn't exist, it will be created automatically when we run the application.

DATABASE_URL = "sqlite:///./blog.db"

# Create the SQLAlchemy engine, which is responsible for managing the connection to the database.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

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