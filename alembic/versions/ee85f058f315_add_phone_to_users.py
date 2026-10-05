"""add phone to users

Revision ID: ee85f058f315
Revises: 5605f9b235d9
Create Date: 2026-09-26 06:21:39.768595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee85f058f315'
down_revision: Union[str, Sequence[str], None] = '5605f9b235d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "phone",
            sa.String(),
            nullable=True,
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","phone")
