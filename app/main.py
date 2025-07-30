import hashlib
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.schema import User, UserCreate, UserResponse, UserUpdate
from app.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url=settings.DOC_URL,
    redoc_url=settings.REDOC_URL,
    description="A simple User API with FastAPI and Scalar integration",
)

# In-memory database (for demo purposes)
users_db: Dict[int, User] = {}
user_id_counter = 1


def hash_password(password: str) -> str:
    """Simple password hashing function"""
    return hashlib.sha256(password.encode()).hexdigest()


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Welcome to User API", "docs": "/scalar"}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user(user: UserCreate):
    """
    Create a new user with validation

    - **name**: User's full name (2-50 characters, letters and spaces only)
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars, must contain uppercase,
    - lowercase, digit, special char)
    """
    global user_id_counter

    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Create new user
    hashed_password = hash_password(user.password)
    new_user = User(
        id=user_id_counter, name=user.name, email=user.email, password=hashed_password
    )

    users_db[user_id_counter] = new_user
    user_id_counter += 1

    return UserResponse(id=new_user.id, name=new_user.name, email=new_user.email)


@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_all_users():
    """Get all users (without passwords)"""
    return [
        UserResponse(id=user.id, name=user.name, email=user.email)
        for user in users_db.values()
    ]


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = users_db[user_id]
    return UserResponse(id=user.id, name=user.name, email=user.email)


@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: UserUpdate):
    """Update a user's information"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = users_db[user_id]

    # Check if email is being changed and if it already exists
    if user_update.email and user_update.email != user.email:
        for existing_user in users_db.values():
            if existing_user.email == user_update.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

    # Update user fields
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email

    users_db[user_id] = user
    return UserResponse(id=user.id, name=user.name, email=user.email)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    del users_db[user_id]
    return


@app.get("/users/search/by-email", response_model=UserResponse, tags=["Users"])
def search_user_by_email(email: str):
    """Search for a user by email address"""
    for user in users_db.values():
        if user.email == email:
            return UserResponse(id=user.id, name=user.name, email=user.email)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "user-api", "total_users": len(users_db)}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    """Scalar API documentation"""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
