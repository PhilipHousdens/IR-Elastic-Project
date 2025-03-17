from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.db import get_db
from model.dbModels import Recipe, UserResponse, UserCreate, User
from utils.passswordHash import hash_password, verify_password  # Assuming these functions are implemented
from utils.JWTToken import verify_token, create_access_token

app = FastAPI()


origins = [
    "http://localhost:5173",  # Add the URL where your frontend is served
]

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define OAuth2PasswordBearer to handle the token extraction from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Define the function that will extract the current user from the database using the JWT token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if user is None:
        raise credentials_exception
    return user

# Endpoint to search recipes by name or ingredient
@app.get("/recipes/search/")
def search_recipes(query: str, db: Session = Depends(get_db)):
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

# Endpoint for user registration
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and save user
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

class LoginRequest(BaseModel):
    username: str
    password: str


# Endpoint for user login and JWT token generation
@app.post("/login")
def login_for_access_token(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
