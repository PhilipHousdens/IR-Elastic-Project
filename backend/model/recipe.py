from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from model.user import User

# Base class for SQLAlchemy models
Base = declarative_base()

# Define Recipe model
class Recipe(Base):
    __tablename__ = 'recipes'
    __table_args__ = {'schema': 'recipes_tb'}
    
    RecipeId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    AuthorId = Column(Integer)
    CookTime = Column(String)
    PrepTime = Column(String)
    TotalTime = Column(String)
    DatePublished = Column(Date)
    Description = Column(String)
    Images = Column(String)
    RecipeCategory = Column(String)
    Keywords = Column(String)
    AggregatedRating = Column(Float)
    ReviewCount = Column(Integer)
    Calories = Column(Integer)
    FatContent = Column(Integer)
    SaturatedFatContent = Column(Integer)
    CholesterolContent = Column(Integer)
    SodiumContent = Column(Integer)
    CarbohydrateContent = Column(Integer)
    FiberContent = Column(Integer)
    SugarContent = Column(Integer)
    ProteinContent = Column(Integer)
    RecipeServings = Column(Integer)
    RecipeYield = Column(String)
    RecipeInstructions = Column(String)
    image_link = Column(String)
    text = Column(String)

# Define Bookmark model
class Bookmark(Base):
    __tablename__ = 'bookmarks'
    __table_args__ = {'schema': 'recipes_tb'} 

    bookmark_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('recipes_tb.users.user_id'))
    recipe_id = Column(Integer, ForeignKey('recipes_tb.recipes.RecipeId'))
    rating = Column(Integer)  # Rating between 1-5
    # You can add more fields here like 'created_at', etc.

    user = relationship("User", back_populates="bookmarks")
    recipe = relationship("Recipe", back_populates="bookmarks")

User.bookmarks = relationship("Bookmark", back_populates="user")
Recipe.bookmarks = relationship("Bookmark", back_populates="recipe")
