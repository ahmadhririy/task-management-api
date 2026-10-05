"""add foreign key indexes

Revision ID: c237a70c04e3
Revises: ee85f058f315
Create Date: 2026-09-29 07:26:47.908886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c237a70c04e3'
down_revision: Union[str, Sequence[str], None] = 'ee85f058f315'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
    "idx_projects_user_id",
    "projects",
    ["user_id"]
     )
    op.create_index(
    "idx_tasks_project_id",
    "tasks",
    ["project_id"]
     )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "idx_tasks_project_id",
        table_name="tasks"
    )

    op.drop_index(
        "idx_projects_user_id",
        table_name="projects"
    )
