# the reason for this empty __init__.py file is to tell python that the "routers" 
# directory is a package. This allows us to import the router modules (like posts.py) 
# from this package in our main application file (main.py). Without this __init__.py file, 
# Python would not recognize the "routers" directory as a package, and we would not be 
# able to import the router modules properly.