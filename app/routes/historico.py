from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Envio, Vaga
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
# HISTÓRICO DE ENVIOS
# =========================

@router.get(
    "/historico_envios",
    response_class=HTMLResponse
)
def historico_envios(
    request: Request,
    db: Session = Depends(get_db)
):

    try:

        envios = (
            db.query(Envio)
            .order_by(Envio.id.desc())
            .all()
        )

        for envio in envios:

            envio.vaga_nome = "-"

            vaga = (
                db.query(Vaga)
                .filter(Vaga.id == envio.vaga_id)
                .first()
            )

            if vaga:
                envio.vaga_nome = vaga.titulo

        return templates.TemplateResponse(
            request=request,
            name="historico_envios.html",
            context={
                "request": request,
                "envios": envios
            }
        )

    except Exception as e:

        print("❌ ERRO HISTÓRICO:")
        print(e)

        return HTMLResponse(
            f"ERRO HISTÓRICO: {str(e)}",
            status_code=500
        )