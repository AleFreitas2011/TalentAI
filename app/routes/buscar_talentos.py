from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Candidato
from app.core.templates import templates


router = APIRouter()


# =========================
# DATABASE
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# BUSCAR TALENTOS
# =========================

@router.get(
    "/buscar_talentos",
    response_class=HTMLResponse
)
def buscar_talentos(
    request: Request,
    q: str = "",
    db: Session = Depends(get_db)
):

    candidatos = db.query(Candidato).all()

    resultados = []

    if q:

        termo = q.strip().lower()

        for candidato in candidatos:

            texto_cv = (candidato.texto_cv or "").lower()
            nome = (candidato.nome_arquivo or "").lower()

            # =========================
            # PRINCIPAIS CONHECIMENTOS
            # Mesma fonte utilizada pelo Consultant 360
            # =========================

            principais_conhecimentos = []

            if candidato.skills_extraidas:

                principais_conhecimentos = [
                    skill.strip()
                    for skill in candidato.skills_extraidas.split(",")
                    if skill.strip()
                ]

            # =========================
            # BUSCA
            # =========================

            texto_skills = " ".join(
                principais_conhecimentos
            ).lower()

            encontrado = (
                termo in texto_cv
                or termo in nome
                or termo in texto_skills
            )

            if encontrado:

                resultados.append({
                    "id": candidato.id,
                    "nome": candidato.nome_arquivo,
                    "principais_conhecimentos": principais_conhecimentos
                })

    return templates.TemplateResponse(
        request=request,
        name="buscar_talentos.html",
        context={
            "request": request,
            "resultados": resultados,
            "q": q
        }
    )