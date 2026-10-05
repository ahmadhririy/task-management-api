"""initial schema

Revision ID: 7d09af13797f
Revises: 
Create Date: 2026-09-26 05:59:03.659850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d09af13797f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
    "users",

    sa.Column(
        "id",
        sa.Integer(),
        sa.Identity(),
        primary_key=True
    ),

    sa.Column(
        "name",
        sa.String(100),
        nullable=False
    ),

    sa.Column(
        "email",
        sa.String(255),
        nullable=False,
        unique=True
    ),

    sa.Column(
        "password_hash",
        sa.String(255),
        nullable=False
    )
    )
    op.create_table(
    "projects",

    sa.Column(
        "id",
        sa.Integer(),
        sa.Identity(),
        primary_key=True
    ),

    sa.Column(
        "name",
        sa.String(100),
        nullable=False
    ),

    sa.Column(
        "description",
        sa.Text(),
        nullable=True
    ),

    sa.Column(
        "user_id",
        sa.Integer(),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    )
    op.create_table(
        "tasks",
    
        sa.Column(
            "id",
            sa.Integer(),
            sa.Identity(),
            primary_key=True
        ),
    
        sa.Column(
            "title",
            sa.String(150),
            nullable=False
        ),
    
        sa.Column(
            "description",
            sa.Text(),
            nullable=True
        ),
        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="todo"
        ),
    
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.CheckConstraint(
        "status IN ('todo', 'in_progress', 'done')",
         name="tasks_status_check"
        )
        )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
    op.drop_table("projects")
    op.drop_table("users")

