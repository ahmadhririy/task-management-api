"""add created_at to users

Revision ID: 5605f9b235d9
Revises: 7d09af13797f
Create Date: 2026-09-26 06:06:56.175211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5605f9b235d9'
down_revision: Union[str, Sequence[str], None] = '7d09af13797f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now()
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "created_at")
