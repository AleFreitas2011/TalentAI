from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Vaga, Candidato
from app.services.agents.executive_briefing_agent import ExecutiveBriefingAgent
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
# DASHBOARD
# =========================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    try:

        # =========================
        # LANGUAGE
        # =========================

        language = getattr(
            request.state,
            "language",
            "pt-BR"
        )

        # =========================
        # KPIs
        # =========================

        total_vagas = (
            db.query(Vaga)
            .filter(Vaga.status == "Aberta")
            .count()
        )

        vagas_finalizadas = (
            db.query(Vaga)
            .filter(Vaga.status == "Fechada")
            .count()
        )

        total_candidatos = (
            db.query(Candidato)
            .count()
        )

        media_score = (
            db.query(Candidato.score)
            .all()
        )

        media_match = 0

        if media_score:

            media_match = round(
                sum(c[0] or 0 for c in media_score) / len(media_score),
                2
            )

        # =========================
        # DASHBOARD V3
        # =========================

        entrevistas_hoje = 0

        vagas_novas = total_vagas

        matches_90 = (
            db.query(Candidato)
            .filter(Candidato.score >= 90)
            .count()
        )

        # =========================
        # TALIA
        # =========================

        briefing_agent = ExecutiveBriefingAgent()

        talia = briefing_agent.build(
            total_vagas=total_vagas,
            vagas_novas=vagas_novas,
            total_candidatos=total_candidatos,
            entrevistas_hoje=entrevistas_hoje,
            matches_90=matches_90,
            media_match=media_match,
            language=language
        )

        # =========================
        # TEMPLATE
        # =========================

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={

                "request": request,

                # Language
                "language": language,

                # Dashboard antigo
                "vagas_abertas": total_vagas,
                "vagas_finalizadas": vagas_finalizadas,
                "media_match": media_match,

                # Dashboard V3
                "total_vagas": total_vagas,
                "vagas_novas": vagas_novas,
                "total_candidatos": total_candidatos,
                "entrevistas_hoje": entrevistas_hoje,
                "matches_90": matches_90,

                # TALIA
                "talia": talia

            }
        )

    except Exception as e:

        print("❌ ERRO DASHBOARD:")
        print(e)

        return HTMLResponse(
            f"ERRO DASHBOARD: {str(e)}",
            status_code=500
        )