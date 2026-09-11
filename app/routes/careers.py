from fastapi import (
    APIRouter,
    Request,
    Depends,
    UploadFile,
    File,
    Form
)

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import SessionLocal
from app.models import Vaga, Cliente
from app.core.templates import templates
from app.services.candidate_processor import processar_candidato

import os


router = APIRouter()


# =====================================================
# DATABASE
# =====================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================================
# TALENTAI CAREERS
# GESTÃO INTERNA POR CLIENTE
# =====================================================

@router.get(
    "/careers/manage",
    response_class=HTMLResponse
)
def careers_manage(
    request: Request,
    db: Session = Depends(get_db)
):

    clientes = (
        db.query(
            Cliente.id,
            Cliente.empresa,
            Cliente.nome_contato,
            func.count(Vaga.id).label("vagas_abertas")
        )
        .join(Vaga, Vaga.cliente_id == Cliente.id)
        .filter(Vaga.status == "Aberta")
        .group_by(
            Cliente.id,
            Cliente.empresa,
            Cliente.nome_contato
        )
        .order_by(
            func.count(Vaga.id).desc(),
            Cliente.empresa.asc()
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="careers_manage.html",
        context={
            "request": request,
            "clientes": clientes
        }
    )


# =====================================================
# TALENTAI CAREERS
# PÁGINA PÚBLICA POR CLIENTE
# =====================================================

@router.get(
    "/careers/client/{cliente_id}",
    response_class=HTMLResponse
)
def careers_by_client(
    cliente_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        return HTMLResponse(
            content="Company not found.",
            status_code=404
        )

    vagas = (
        db.query(Vaga)
        .filter(
            Vaga.status == "Aberta",
            Vaga.cliente_id == cliente_id
        )
        .order_by(Vaga.data_criacao.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="careers.html",
        context={
            "request": request,
            "vagas": vagas,
            "cliente": cliente
        }
    )


# =====================================================
# TALENTAI CAREERS
# PÁGINA PÚBLICA DE VAGAS
# =====================================================

@router.get(
    "/careers",
    response_class=HTMLResponse
)
def careers(
    request: Request,
    db: Session = Depends(get_db)
):

    vagas = (
        db.query(Vaga)
        .filter(Vaga.status == "Aberta")
        .order_by(Vaga.data_criacao.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="careers.html",
        context={
            "request": request,
            "vagas": vagas,
            "cliente": None
        }
    )


# =====================================================
# TALENTAI CAREERS
# DETALHE PÚBLICO DA VAGA
# =====================================================

@router.get(
    "/careers/job/{vaga_id}",
    response_class=HTMLResponse
)
def career_job_detail(
    vaga_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    vaga = (
        db.query(Vaga)
        .filter(
            Vaga.id == vaga_id,
            Vaga.status == "Aberta"
        )
        .first()
    )

    if not vaga:

        return HTMLResponse(
            content="Opportunity not found.",
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="career_job_detail.html",
        context={
            "request": request,
            "vaga": vaga
        }
    )


# =====================================================
# TALENTAI CAREERS
# FORMULÁRIO PÚBLICO DE CANDIDATURA
# =====================================================

@router.get(
    "/careers/job/{vaga_id}/apply",
    response_class=HTMLResponse
)
def career_apply(
    vaga_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    vaga = (
        db.query(Vaga)
        .filter(
            Vaga.id == vaga_id,
            Vaga.status == "Aberta"
        )
        .first()
    )

    if not vaga:

        return HTMLResponse(
            content="Opportunity not found.",
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="career_apply.html",
        context={
            "request": request,
            "vaga": vaga
        }
    )


# =====================================================
# TALENTAI CAREERS
# RECEBER CANDIDATURA
# =====================================================

@router.post(
    "/careers/job/{vaga_id}/apply",
    response_class=HTMLResponse
)
async def career_apply_submit(
    vaga_id: int,
    request: Request,

    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),

    curriculo: UploadFile = File(...),

    db: Session = Depends(get_db)
):

    # =================================================
    # VALIDAR VAGA
    # =================================================

    vaga = (
        db.query(Vaga)
        .filter(
            Vaga.id == vaga_id,
            Vaga.status == "Aberta"
        )
        .first()
    )

    if not vaga:

        return HTMLResponse(
            content="Opportunity not found.",
            status_code=404
        )


    # =================================================
    # VALIDAR PDF
    # =================================================

    nome_arquivo = curriculo.filename or ""

    if not nome_arquivo.lower().endswith(".pdf"):

        return templates.TemplateResponse(
            request=request,
            name="career_apply.html",
            context={
                "request": request,
                "vaga": vaga,
                "erro": "PDF_REQUIRED"
            },
            status_code=400
        )


    # =================================================
    # SALVAR CV
    # =================================================

    pasta_upload = "uploads_careers"

    os.makedirs(
        pasta_upload,
        exist_ok=True
    )

    nome_seguro = os.path.basename(
        nome_arquivo
    ).replace(
        " ",
        "_"
    )

    caminho_cv = os.path.join(
        pasta_upload,
        nome_seguro
    )

    conteudo = await curriculo.read()

    with open(
        caminho_cv,
        "wb"
    ) as arquivo_destino:

        arquivo_destino.write(
            conteudo
        )


    # =================================================
    # PROCESSAR CANDIDATO
    # PIPELINE OFICIAL TALENTAI / TALIA
    # =================================================

    candidato = processar_candidato(
        arquivo=curriculo,
        vaga=vaga,
        caminho_cv=caminho_cv,
        db=db,
        origem="TalentAI Careers",
        email_confirmado=email,
        telefone_confirmado=telefone
    )


    # =================================================
    # DUPLICIDADE
    # =================================================

    if candidato is None:

        return templates.TemplateResponse(
            request=request,
            name="career_apply.html",
            context={
                "request": request,
                "vaga": vaga,
                "erro": "APPLICATION_NOT_PROCESSED"
            },
            status_code=400
        )


    # =================================================
    # DADOS CONFIRMADOS
    # =================================================
    #
    # E-mail, telefone e origem já foram entregues ao
    # candidate_processor antes da identificação do talento.
    # Assim, Careers não sobrescreve o cadastro depois que
    # a candidatura foi criada.
    # =================================================

    # =================================================
    # SUCESSO
    # =================================================

    return templates.TemplateResponse(
        request=request,
        name="career_application_success.html",
        context={
            "request": request,
            "vaga": vaga,
            "candidato": candidato,
            "nome_candidato": nome.strip()
        }
    )
