from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from model.models import Recipe

app = FastAPI()

# Endpoint to search recipes by name or ingredient
@app.get("/recipes/search/")
def search_recipes(query: str, db: Session = Depends(get_db)):
    # Perform a search query on the recipe name or ingredient
    results = db.query(Recipe).filter(Recipe.Name.ilike(f"%{query}%")).all()
    return results

# Endpoint to get all recipes
@app.get("/recipes/")
def get_all_recipes(db: Session = Depends(get_db)):
    try:
        recipes = db.query(Recipe).all()
        return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get a recipe by its ID
@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    try:
        recipe = db.query(Recipe).filter(Recipe.RecipeId == recipe_id).first()
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
