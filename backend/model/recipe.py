from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

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

    bookmarks = relationship("Bookmark", back_populates="recipe")

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    __table_args__ = {'schema': 'recipes_tb'} 

    bookmark_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Correct table reference
    recipe_id = Column(Integer, ForeignKey('recipes_tb.recipes.RecipeId'))
    rating = Column(Integer)  # Rating between 1-5

    @declared_attr
    def user(cls):
        from model.user import User  # Import inside the class
        return relationship("User", back_populates="bookmarks")

    recipe = relationship("Recipe", back_populates="bookmarks")
