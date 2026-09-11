from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Cliente, Vaga, Candidato, Envio
from app.ai.client import client
from app.core.templates import templates

from typing import List
import urllib.parse

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
# VAGAS
# =========================

@router.get(
    "/vagas",
    response_class=HTMLResponse
)
def listar_vagas(
    request: Request,
    db: Session = Depends(get_db)
):

    vagas_ativas = (
        db.query(Vaga)
        .filter(Vaga.status == "Aberta")
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="vagas.html",
        context={
            "request": request,
            "vagas_ativas": vagas_ativas,
        }
    )   

# =========================
# NOVA VAGA (TELA)
# =========================

@router.get(
    "/nova_vaga",
    response_class=HTMLResponse
)
def tela_nova_vaga(
    request: Request,
    db: Session = Depends(get_db)
):

    clientes = db.query(Cliente).all()

    return templates.TemplateResponse(
        request=request,
        name="nova_vaga.html",
        context={
            "request": request,
            "clientes": clientes
        }
    )

# =========================
# NOVA VAGA (SALVAR)
# =========================

@router.post("/nova_vaga")
def nova_vaga(
    request: Request,
    titulo: str = Form(...),
    cliente_id: int = Form(...),
    descricao: str = Form(""),
    palavras_chave: str = Form(""),
    status: str = Form("Aberta"),
    db: Session = Depends(get_db)
):

    if not request.session.get("user_id"):
        return RedirectResponse(
            "/login",
            status_code=302
        )

    vaga = Vaga(
        titulo=titulo,
        cliente_id=cliente_id,
        descricao=descricao,
        palavras_chave=palavras_chave,
        status=status,
        usuario_id=request.session.get("user_id")
    )

    db.add(vaga)
    db.commit()

    return RedirectResponse(
        "/",
        status_code=303
    )

# =========================
# FECHAR VAGA
# =========================

@router.get("/fechar_vaga/{vaga_id}")
def fechar_vaga(
    vaga_id: int,
    db: Session = Depends(get_db)
):

    vaga = (
        db.query(Vaga)
        .filter(Vaga.id == vaga_id)
        .first()
    )

    if vaga:
        vaga.status = "Fechada"
        db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@router.get("/reabrir_vaga/{vaga_id}")
def reabrir_vaga(
    vaga_id: int,
    db: Session = Depends(get_db)
):

    vaga = (
        db.query(Vaga)
        .filter(Vaga.id == vaga_id)
        .first()
    )

    if vaga:

        vaga.status = "Aberta"

        db.commit()

    return RedirectResponse(
        url="/vagas_encerradas",
        status_code=303
    )

@router.get(
    "/vagas_encerradas",
    response_class=HTMLResponse
)
def vagas_encerradas(
    request: Request,
    db: Session = Depends(get_db)
):

    vagas = (
        db.query(Vaga)
        .filter(Vaga.status == "Fechada")
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="vagas_encerradas.html",
        context={
            "request": request,
            "vagas": vagas
        }
    )

# =========================
# EDITAR VAGA (ABRIR TELA)
# =========================

@router.get("/editar_vaga/{vaga_id}")
def editar_vaga_form(
    vaga_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    vaga = (
        db.query(Vaga)
        .filter(
            Vaga.id == vaga_id,
            Vaga.usuario_id == user_id
        )
        .first()
    )

    if not vaga:
        return RedirectResponse(
            "/",
            status_code=303
        )

    clientes = db.query(Cliente).all()

    return templates.TemplateResponse(
        "editar_vaga.html",
        {
            "request": request,
            "vaga": vaga,
            "clientes": clientes
        }
    )


# =========================
# EDITAR VAGA (SALVAR)
# =========================

@router.post("/editar_vaga")
def editar_vaga_salvar(
    request: Request,
    vaga_id: int = Form(...),
    titulo: str = Form(...),
    cliente_id: int = Form(...),
    descricao: str = Form(""),
    palavras_chave: str = Form(""),
    status: str = Form("Aberta"),
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            "/login",
            status_code=302
        )

    vaga = (
        db.query(Vaga)
        .filter(
            Vaga.id == vaga_id,
            Vaga.usuario_id == user_id
        )
        .first()
    )

    if not vaga:
        return RedirectResponse(
            "/",
            status_code=303
        )

    vaga.titulo = titulo
    vaga.cliente_id = cliente_id
    vaga.descricao = descricao
    vaga.palavras_chave = palavras_chave
    vaga.status = status

    db.commit()
    db.refresh(vaga)

    return RedirectResponse(
        url=f"/vaga/{vaga.id}",
        status_code=303
    )

@router.get("/duplicar_vaga/{vaga_id}")
def duplicar_vaga(
    vaga_id: int,
    db: Session = Depends(get_db)
):

    vaga_original = (
        db.query(Vaga)
        .filter(Vaga.id == vaga_id)
        .first()
    )

    if not vaga_original:
        return RedirectResponse(
            url="/vagas_encerradas",
            status_code=303
        )

    nova_vaga = Vaga(

        titulo=vaga_original.titulo,

        cliente_id=vaga_original.cliente_id,

        descricao=vaga_original.descricao,

        palavras_chave=vaga_original.palavras_chave,

        status="Aberta",

        usuario_id=vaga_original.usuario_id

    )

    db.add(nova_vaga)

    db.commit()

    db.refresh(nova_vaga)

    return RedirectResponse(
        url=f"/vaga/{nova_vaga.id}",
        status_code=303
    )

# =========================
# ENVIAR CLIENTE
# =========================

@router.post("/enviar_cliente/{vaga_id}")
def enviar_cliente(
    vaga_id: int,
    request: Request,
    candidatos_ids: List[int] = Form(default=[]),
    cliente_id: int = Form(...),
    idioma: str = Form("PT"),
    db: Session = Depends(get_db)
):

    if not candidatos_ids:
        return RedirectResponse(
            url=f"/vaga/{vaga_id}",
            status_code=303
        )

    vaga = db.query(Vaga).filter(
        Vaga.id == vaga_id
    ).first()

    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not vaga or not cliente:
        return RedirectResponse(
            url=f"/vaga/{vaga_id}",
            status_code=303
        )

    candidatos = db.query(Candidato).filter(
        Candidato.id.in_(candidatos_ids)
    ).all()

    conteudo_email = ""

    if idioma == "EN":

        conteudo_email += f"""Hi {cliente.nome_contato.split()[0] if cliente.nome_contato else "Client"},

Please find below the candidates for the position: {vaga.titulo}
"""

    else:

        conteudo_email += f"""Olá {cliente.nome_contato.split()[0] if cliente.nome_contato else "Cliente"},

Segue abaixo os candidatos para a vaga: {vaga.titulo}
"""

    for c in candidatos:

        c.etapa = "Enviado"

        if idioma == "EN":

            email_candidato = c.email or "-"

            if email_candidato.strip().lower() == "não encontrado":
                email_candidato = "Not found"

            conteudo_email += f"""

Candidate: {c.nome_arquivo}
Match Score: {c.score or 0}%

Summary:
{c.resumo or "No summary"}

Email: {email_candidato}
Phone: {c.telefone or "-"}
"""

        else:

            conteudo_email += f"""

Candidato: {c.nome_arquivo}
Aderência: {c.score or 0}%

Resumo:
{c.resumo or "Sem resumo"}

Email: {c.email or "-"}
Telefone: {c.telefone or "-"}
"""

    if idioma == "EN":
        conteudo_email += "\n\nHappy to discuss next steps."
    else:
        conteudo_email += "\n\nFico à disposição para próximos passos."

    envio = Envio(
        vaga_id=vaga_id,
        cliente_id=cliente_id,
        candidatos=", ".join(
            [c.nome_arquivo for c in candidatos]
        )
    )

    db.add(envio)
    db.commit()

    link = (
        f"https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={cliente.email}"
        f"&su={urllib.parse.quote('Candidatos - ' + vaga.titulo)}"
        f"&body={urllib.parse.quote(conteudo_email)}"
    )

    return RedirectResponse(
        url=link,
        status_code=302
    )

@router.get(
    "/vagas_encerradas",
    response_class=HTMLResponse
)
def vagas_encerradas(
    request: Request,
    db: Session = Depends(get_db)
):

    vagas = (
        db.query(Vaga)
        .filter(Vaga.status == "Fechada")
        .all()
    )

    return templates.TemplateResponse(
        "vagas_encerradas.html",
        {
            "request": request,
            "vagas": vagas
        }
    )

# =========================
# ✨ GERAR ANUNCIO IA
# =========================

@router.get("/gerar_anuncio_ia/{vaga_id}", response_class=HTMLResponse)
def gerar_anuncio_ia(
    request: Request,
    vaga_id: int,
    db: Session = Depends(get_db)
):

    vaga = (
        db.query(Vaga)
        .filter(Vaga.id == vaga_id)
        .first()
    )

    if not vaga:
        return HTMLResponse(
            "Vaga não encontrada",
            status_code=404
        )

    # =========================
    # IDIOMA ATUAL
    # =========================

    language = getattr(
        request.state,
        "language",
        "pt-BR"
    )

    # =========================
    # PROMPT POR IDIOMA
    # =========================

    if language == "en-US":

        prompt = f"""
Create a professional and attractive LinkedIn job advertisement
for the following position.

Job Title:
{vaga.titulo}

Job Description:
{vaga.descricao}

The advertisement must:
- be written entirely in English
- be modern and professional
- be clearly organized
- use emojis moderately
- highlight the main requirements
- highlight the main responsibilities
- preserve important technical terms
- end with a clear call to action
"""

    else:

        prompt = f"""
Crie um anúncio profissional e atrativo para LinkedIn
para a seguinte vaga.

Título:
{vaga.titulo}

Descrição:
{vaga.descricao}

O anúncio deve:
- ser escrito inteiramente em português do Brasil
- ser moderno e profissional
- ser claramente organizado
- usar emojis moderadamente
- destacar os principais requisitos
- destacar as principais responsabilidades
- preservar termos técnicos importantes
- terminar com uma chamada para ação
"""

    # =========================
    # GERAR ANUNCIO
    # =========================

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        anuncio = response.choices[0].message.content

    except Exception as e:

        print("❌ ERRO IA ANUNCIO:")
        print(e)

        if language == "en-US":
            anuncio = "Error generating AI job advertisement."
        else:
            anuncio = "Erro ao gerar anúncio com IA."

    # =========================
    # RESULTADO
    # =========================

    return templates.TemplateResponse(
        request=request,
        name="resultado_ia.html",
        context={
            "request": request,
            "vaga": vaga,
            "anuncio": anuncio
        }
    )