"""상담 티켓 표 구조를 변경합니다."""
from alembic import op
import sqlalchemy as sa

revision = "20260911_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS ch31_migration")
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question", sa.String(length=200), nullable=False),
        schema="ch31_migration",
    )


def downgrade() -> None:
    op.drop_table("tickets", schema="ch31_migration")
