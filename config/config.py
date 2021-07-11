import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

class GroceryConfig(Config):
    DB_URI =  "sqlite:///" + os.path.join(basedir, "..","website",  "grocery_data.sqlite")
    
class ClothingConfig(Config):
    DB_URI =  "sqlite:///" + os.path.join(basedir, "..","website",  "clothing_data.sqlite")
    
class AccessoriesConfig(Config):
    DB_URI =  "sqlite:///" + os.path.join(basedir, "..","website",  "pc_data.sqlite")
    
