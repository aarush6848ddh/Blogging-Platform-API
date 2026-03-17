from fastapi import FastAPI
from database import engine # this imports the database engine we created in database.py, which is responsible for managing the connection to our SQLite database.
import models # this imports the models we defined in models.py, which represent the structure of our database tables. We need to import this so that SQLAlchemy can create the tables in the database based on these models.
from routers import posts # this imports the posts router we defined in routers/posts.py, which contains all the API endpoints related to blog posts. By importing this, we can include it in our FastAPI application and make those endpoints available to handle incoming requests.

# This creates a new FastAPI application instance. 
# The title, description, and version parameters are 
# optional metadata that can be used for documentation 
# purposes. They will appear in the automatically 
# generated API docs provided by FastAPI.
app = FastAPI(title="Blogging Platform API", description="API for managing blog posts, comments, and user profiles.", version="1.0.0")

# This line creates the database tables based on the models defined in the models.py file.
# The create_all method checks the metadata of the models and creates the corresponding 
# tables in the database
models.Base.metadata.create_all(bind=engine)

# This line includes the router defined in the posts.py file.
# By including this router, we are telling our FastAPI application 
# to use the endpoints defined in posts.py for handling requests that 
# start with the prefix "/posts".
app.include_router(posts.router)
