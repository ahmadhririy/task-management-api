from fastapi import APIRouter, Depends, status, HTTPException

from app.database import get_connection
from app.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: ProjectCreate,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO projects (name, description, user_id)
                VALUES (%s, %s, %s)
                RETURNING id, name, description, user_id;
                """,
                (
                    project.name,
                    project.description,
                    current_user["id"]
                )
            )

            new_project = cursor.fetchone()

    return new_project


@router.get("", response_model=list[ProjectResponse])
def get_projects(
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, user_id
                FROM projects
                WHERE user_id = %s
                """,
                (current_user["id"],)
            )

            projects = cursor.fetchall()

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, user_id
                FROM projects
                WHERE id = %s AND user_id = %s
                """,
                (
                    project_id,
                    current_user["id"]
                )
            )

            project = cursor.fetchone()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, user_id
                FROM projects
                WHERE id = %s AND user_id = %s
                """,
                (
                    project_id,
                    current_user["id"]
                )
            )

            existing_project = cursor.fetchone()

            if not existing_project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found"
                )

            update_data = project.model_dump(exclude_unset=True)

            new_name = update_data.get(
                "name",
                existing_project["name"]
            )

            new_description = update_data.get(
                "description",
                existing_project["description"]
            )

            cursor.execute(
                """
                UPDATE projects
                SET name = %s,
                    description = %s
                WHERE id = %s AND user_id = %s
                RETURNING id, name, description, user_id;
                """,
                (
                    new_name,
                    new_description,
                    project_id,
                    current_user["id"]
                )
            )

            updated_project = cursor.fetchone()

    return updated_project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM projects
                WHERE id = %s AND user_id = %s
                RETURNING id;
                """,
                (
                    project_id,
                    current_user["id"]
                )
            )

            deleted_project = cursor.fetchone()

            if not deleted_project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found"
                )

    return {
        "message": "Project deleted successfully"
    }