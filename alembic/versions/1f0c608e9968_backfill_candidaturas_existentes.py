"""backfill candidaturas existentes

Revision ID: 1f0c608e9968
Revises: 44a1db520e0c
Create Date: 2026-09-02 17:38:43.642784

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f0c608e9968"
down_revision: Union[str, Sequence[str], None] = "44a1db520e0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Preserva na nova tabela candidaturas os relacionamentos
    Candidato x Vaga que já existem no TalentAI.

    Nesta etapa:
    - candidatos não são removidos;
    - vaga_id legado não é alterado;
    - scores e análises atuais continuam intactos;
    - somente candidatos que possuem vaga_id são copiados.
    """

    op.execute(
        sa.text(
            """
            INSERT INTO candidaturas (
                candidato_id,
                vaga_id,
                origem,
                status,
                match_score,
                match_data,
                data_candidatura,
                data_atualizacao
            )
            SELECT
                c.id,
                c.vaga_id,
                c.origem,
                c.etapa,
                CAST(c.score AS INTEGER),
                c.dados_ia,
                COALESCE(c.data_upload, CURRENT_TIMESTAMP),
                NULL
            FROM candidatos AS c
            WHERE c.vaga_id IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1
                  FROM candidaturas AS ca
                  WHERE ca.candidato_id = c.id
                    AND ca.vaga_id = c.vaga_id
              )
            """
        )
    )


def downgrade() -> None:
    """
    Remove somente as candidaturas correspondentes ao
    relacionamento legado atualmente registrado em candidatos.

    Não remove candidatos nem vagas.
    """

    op.execute(
        sa.text(
            """
            DELETE FROM candidaturas
            WHERE EXISTS (
                SELECT 1
                FROM candidatos AS c
                WHERE c.id = candidaturas.candidato_id
                  AND c.vaga_id = candidaturas.vaga_id
            )
            """
        )
    )