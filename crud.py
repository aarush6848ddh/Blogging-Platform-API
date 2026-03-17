from sqlalchemy.orm import Session
import models
import schemas

# This function creates a new post in the database. 
# It takes a SQLAlchemy session and a PostCreate schema as input, 
# creates a new Post model instance, adds it to the session, 
# commits the transaction to save it to the database, 
# and then refreshes the instance to get the updated data 
# (like the generated ID) before returning it.
def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# This function retrieves all posts from the database that 
# contain the search string in their title.
def get_posts(db: Session, search: str = ""):
    return db.query(models.Post).filter(models.Post.title.contains(search)).all()

# This function retrieves a single post by its ID. 
# It returns the post if found, or None if no post 
# with the given ID exists in the database.
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

# This function updates an existing post in the database.
# It first retrieves the post by its ID. If the post does not exist, 
# it returns None. If the post exists, it updates the fields of the 
# post with the data provided in the PostUpdate schema, commits the 
# changes to the database, refreshes the instance to get the updated 
# data, and then returns the updated post.
def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if db_post is None:
        return None
    update_data = post.model_dump(exclude_unset=True) # exclude_unset=True means that only the fields that were provided in the update request will be included in the update_data dictionary. Without this, if the user only provided a new title but left the content and category fields empty, those fields would be included in the update_data with a value of None, which would overwrite the existing values in the database. By using exclude_unset=True, we ensure that only the fields that the user actually wants to update will be included in the update_data, preventing unintended overwrites of existing data.
    for key, value in update_data.items():
        setattr(db_post, key, value) # setattr is a built-in Python function that sets the value of an attribute of an object. In this case, we are using it to update the fields of the db_post instance with the new values provided in the update_data dictionary. For each key-value pair in the update_data, setattr will set the attribute of db_post corresponding to the key to the new value. This allows us to dynamically update only the fields that were provided in the update request without needing to write separate code for each field.
    db.commit()
    db.refresh(db_post)
    return db_post

# This function deletes a post from the database. 
# It first retrieves the post by its ID.
# If the post does not exist, it returns None.
def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()
    return db_post