from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import UserCreate, UserResponse, UserLogin
from app.database import get_connection
from app.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                """,
                (user.email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            hashed_password = hash_password(user.password)

            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, name, email;
                """,
                (user.name, user.email, hashed_password)
            )

            new_user = cursor.fetchone()

    return new_user


@router.post("/login")
def user_login(user: UserLogin):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash
                FROM users
                WHERE email = %s
                """,
                (user.email,)
            )

            db_user = cursor.fetchone()

            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="email or password is invalid"
                )

            if not verify_password(
                user.password,
                db_user["password_hash"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="email or password is invalid"
                )

            token = create_access_token(db_user["id"])

            return {
                "access_token": token,
                "token_type": "bearer"
            }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user