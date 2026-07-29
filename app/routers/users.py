from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.security import create_access_token, verify_password
from app.crud.user import (
    create_user_with_password,
    get_user,
    get_user_by_email,
    get_user_by_username,
    get_user_profile,
    update_user,
)
from app.database import get_db
from app.models.models import User
from app.schemas.user import (
    Token,
    UserCreate,
    UserProfileRead,
    UserRead,
    UserRegister,
    UserUpdate,
)

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(*, db: Session = Depends(get_db), user_in: UserRegister):
    """POST /api/users/register

    Register a new user account with hashed password.
    """
    if get_user_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user_with_password(db=db, user=user_in)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(*, db: Session = Depends(get_db), user_in: UserCreate):
    """Fallback endpoint POST /api/users/ to create user."""
    if get_user_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user_with_password(db=db, user=user_in)


@router.post("/login", response_model=Token)
def login_for_access_token(
    *, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """POST /api/users/login

    Authenticate user using OAuth2 form data (username & password) and return JWT access token.
    """
    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.username)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead)
def read_user_me(current_user: User = Depends(get_current_user)):
    """GET /api/users/me

    Fetch currently authenticated user profile.
    """
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    """PUT /api/users/me

    Update currently authenticated user details (full_name, email, password).
    """
    if user_update.email and user_update.email != current_user.email:
        existing_user = get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use by another account",
            )
    return update_user(db=db, db_user=current_user, user_update=user_update)


@router.get("/{user_id}", response_model=UserRead)
def read_user(*, db: Session = Depends(get_db), user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{username}/profile", response_model=UserProfileRead)
def read_user_profile(*, db: Session = Depends(get_db), username: str):
    """GET /api/users/{username}/profile

    Get user profile along with eager-loaded projects and assigned tasks.
    """
    db_user = get_user_profile(db=db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
