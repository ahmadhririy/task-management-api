from fastapi import APIRouter, HTTPException, Depends, status

from app.database import get_connection
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"]
)
def get_owned_project(cursor, project_id: int, user_id: int):
    cursor.execute(
        """
        SELECT id
        FROM projects
        WHERE id = %s AND user_id = %s
        """,
        (
            project_id,
            user_id
        )
    )

    project = cursor.fetchone()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project



@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    project_id: int,
    task: TaskCreate,
    current_user=Depends(get_current_user)
    ):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            get_owned_project(
                cursor,
                project_id,
                current_user["id"]
            )

            cursor.execute(
                """
                INSERT INTO tasks (title, description, status, project_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, title, description, status, project_id;
                """,
                (
                    task.title,
                    task.description,
                    task.status,
                    project_id
                )
            )

            new_task = cursor.fetchone()

    return new_task


@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    project_id: int,
    current_user=Depends(get_current_user)
    ):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            get_owned_project(
            cursor,
            project_id,
            current_user["id"]
            )

            cursor.execute(
                """
                SELECT id, title, description, status, project_id
                FROM tasks
                WHERE project_id = %s
                """,
                (project_id,)
            )

            tasks = cursor.fetchall()

    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    project_id: int,
    task_id: int,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            get_owned_project(
                cursor,
                project_id,
                current_user["id"]
            )
            cursor.execute(
                """
                SELECT id, title, description, status, project_id
                FROM tasks
                WHERE id = %s AND project_id = %s
                """,
                (
                    task_id,
                    project_id
                )
            )

            task = cursor.fetchone()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    project_id: int,
    task_id: int,
    task: TaskUpdate,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            get_owned_project(
                cursor,
                project_id,
                current_user["id"]
            )

            cursor.execute(
                """
                SELECT id, title, description, status, project_id
                FROM tasks
                WHERE id = %s AND project_id = %s
                """,
                (
                    task_id,
                    project_id
                )
            )

            existing_task = cursor.fetchone()

            if not existing_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            update_data = task.model_dump(exclude_unset=True)

            new_title = update_data.get(
                "title",
                existing_task["title"]
            )

            new_description = update_data.get(
                "description",
                existing_task["description"]
            )

            new_status = update_data.get(
                "status",
                existing_task["status"]
            )

            cursor.execute(
                """
                UPDATE tasks
                SET title = %s,
                    description = %s,
                    status = %s
                WHERE id = %s AND project_id = %s
                RETURNING id, title, description, status, project_id;
                """,
                (
                    new_title,
                    new_description,
                    new_status,
                    task_id,
                    project_id
                )
            )

            updated_task = cursor.fetchone()

    return updated_task



@router.delete("/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    current_user=Depends(get_current_user)
):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            get_owned_project(
                cursor,
                project_id,
                current_user["id"]
            )

            cursor.execute(
                """
                DELETE FROM tasks
                WHERE id = %s AND project_id = %s
                RETURNING id;
                """,
                (
                    task_id,
                    project_id
                )
            )

            deleted_task = cursor.fetchone()

            if not deleted_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

    return {
        "message": "Task deleted successfully"
    }