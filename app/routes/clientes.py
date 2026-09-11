from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Cliente, Vaga
from app.core.templates import templates


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
# LISTAR CLIENTES
# =====================================================

@router.get(
    "/clientes",
    response_class=HTMLResponse
)
def listar_clientes(
    request: Request,
    db: Session = Depends(get_db)
):

    clientes = (
        db.query(Cliente)
        .order_by(Cliente.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="clientes.html",
        context={
            "request": request,
            "clientes": clientes
        }
    )


# =====================================================
# CADASTRAR CLIENTE PELA TELA CLIENTES
# =====================================================

@router.post("/clientes")
def cadastrar_cliente(
    nome_contato: str = Form(...),
    email: str = Form(...),
    empresa: str = Form(""),
    db: Session = Depends(get_db)
):

    cliente = Cliente(
        nome_contato=nome_contato,
        email=email,
        empresa=empresa
    )

    db.add(cliente)
    db.commit()

    return RedirectResponse(
        url="/clientes",
        status_code=303
    )


# =====================================================
# NOVO CLIENTE
# =====================================================

@router.get(
    "/novo_cliente",
    response_class=HTMLResponse
)
def tela_novo_cliente(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="novo_cliente.html",
        context={
            "request": request
        }
    )


# =====================================================
# SALVAR NOVO CLIENTE
# =====================================================

@router.post("/novo_cliente")
def criar_cliente(
    nome_contato: str = Form(...),
    email: str = Form(...),
    empresa: str = Form(...),
    db: Session = Depends(get_db)
):

    cliente = Cliente(
        nome_contato=nome_contato,
        email=email,
        empresa=empresa
    )

    db.add(cliente)
    db.commit()

    return RedirectResponse(
        url="/nova_vaga",
        status_code=303
    )


# =====================================================
# VAGAS POR CLIENTE
# =====================================================

@router.get(
    "/vagas/cliente/{cliente_id}",
    response_class=HTMLResponse
)
def vagas_por_cliente(
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
            "Cliente não encontrado.",
            status_code=404
        )

    vagas = (
        db.query(Vaga)
        .filter(Vaga.cliente_id == cliente_id)
        .order_by(Vaga.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="vagas_cliente.html",
        context={
            "request": request,
            "cliente": cliente,
            "vagas": vagas
        }
    )