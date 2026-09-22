from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import UserCreate, UserResponse, UserLogin ,UserUpdate,PasswordUpdate
from app.database import get_connection
from app.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user
from app.security import verify_password, hash_password


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

@router.patch("/me", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    current_user=Depends(get_current_user)
):
    update_data = user_update.model_dump(exclude_unset=True)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            if "email" in update_data:
             cursor.execute(
                """
                SELECT id, email
                FROM users
                WHERE email = %s AND id != %s
                """,
                (
                    update_data["email"],
                    current_user["id"],
                )
             )
             email_exists = cursor.fetchone()
             if email_exists:
                 raise HTTPException(
                     status_code=status.HTTP_400_BAD_REQUEST,
                     detail="Email already registered"
                 )
            new_name = update_data.get("name", current_user["name"])
            new_email = update_data.get("email", current_user["email"])
            
            cursor.execute(
                     """UPDATE users
                     SET name = %s  ,email =%s
                     where id = %s
                     RETURNING id , name , email""",
                     (new_name,new_email,current_user["id"])
            )
            updated_user = cursor.fetchone()

    return updated_user
                
@router.patch("/me/password")
def update_password(
    password_update: PasswordUpdate,
    current_user=Depends(get_current_user)
):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT password_hash
                FROM users
                WHERE id = %s
                """,
                (current_user["id"],)
            )
            user = cursor.fetchone()
            if not verify_password(
               password_update.current_password,
                 user["password_hash"]
            ):
             raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail="Current password is incorrect"
             )
            new_password_hash = hash_password(password_update.new_password)
            cursor.execute(
             """
               UPDATE users
               SET password_hash = %s
                WHERE id = %s
                 """,
                (
                    new_password_hash,
                     current_user["id"]
                  )
            )
    return {"message": "Password updated successfully"}

@router.delete("/me")
def delete_user(
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """DELETE FROM users
                WHERE id = %s""",
                (current_user["id"],)
            )
    return {"message": "Account deleted successfully"}
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user