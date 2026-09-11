"""cria tabela candidaturas talent bank

Revision ID: 44a1db520e0c
Revises: 1e06834096f7
Create Date: 2026-09-02 16:57:50.831077

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "44a1db520e0c"
down_revision: Union[str, Sequence[str], None] = "1e06834096f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Cria a estrutura inicial de candidaturas do Talent Bank.

    Nesta etapa, nenhuma coluna existente de candidatos
    ou vagas é removida ou alterada.
    """

    op.create_table(
        "candidaturas",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "candidato_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "vaga_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "origem",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=True,
        ),

        sa.Column(
            "match_score",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "match_data",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "data_candidatura",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),

        sa.Column(
            "data_atualizacao",
            sa.DateTime(),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["candidato_id"],
            ["candidatos.id"],
            name="fk_candidaturas_candidato_id",
        ),

        sa.ForeignKeyConstraint(
            ["vaga_id"],
            ["vagas.id"],
            name="fk_candidaturas_vaga_id",
        ),
    )

    op.create_index(
        "ix_candidaturas_candidato_id",
        "candidaturas",
        ["candidato_id"],
        unique=False,
    )

    op.create_index(
        "ix_candidaturas_vaga_id",
        "candidaturas",
        ["vaga_id"],
        unique=False,
    )

    op.create_index(
        "ix_candidaturas_status",
        "candidaturas",
        ["status"],
        unique=False,
    )

    op.create_index(
        "uq_candidaturas_candidato_vaga",
        "candidaturas",
        ["candidato_id", "vaga_id"],
        unique=True,
    )


def downgrade() -> None:
    """
    Remove somente a estrutura criada por esta migration.
    """

    op.drop_index(
        "uq_candidaturas_candidato_vaga",
        table_name="candidaturas",
    )

    op.drop_index(
        "ix_candidaturas_status",
        table_name="candidaturas",
    )

    op.drop_index(
        "ix_candidaturas_vaga_id",
        table_name="candidaturas",
    )

    op.drop_index(
        "ix_candidaturas_candidato_id",
        table_name="candidaturas",
    )

    op.drop_table("candidaturas")