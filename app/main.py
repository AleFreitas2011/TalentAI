from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import tempfile
import json

from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from app.middleware.localization import LocalizationMiddleware
from app.core.jinja import configure_jinja
from app.core.templates import templates

from .db import SessionLocal, engine, Base
from .models import Vaga, Usuario, Cliente, Candidato, Envio

from app.services.cv_parser import extrair_texto_cv
from app.services.email_extractor import extrair_email
from app.services.phone_extractor import extrair_telefone
from app.services.match import calcular_match
from app.services.ai_match import analisar_cv_com_ia
from app.services.candidate_processor import processar_candidato

from app.routes.buscar_talentos import router as buscar_talentos_router
from app.routes.clientes import router as clientes_router
from app.routes.dashboard import router as dashboard_router
from app.routes.historico import router as historico_router
from app.routes.vagas import router as vagas_router
from app.routes.talentos import router as talentos_router
from app.routes.detalhe_vaga import router as detalhe_vaga_router
from app.routes.workspace import router as workspace_router
from app.routes.careers import router as careers_router


app = FastAPI()

print("🔥 CODIGO NOVO RODANDO 🔥")

# =========================
# 🚀 APP
# =========================

app.include_router(buscar_talentos_router)
app.include_router(clientes_router)
app.include_router(dashboard_router)
app.include_router(historico_router)
app.include_router(vagas_router)
app.include_router(talentos_router)
app.include_router(detalhe_vaga_router)
app.include_router(workspace_router)
app.include_router(careers_router)

# =========================
# MIDDLEWARES
# =========================

app.add_middleware(
    LocalizationMiddleware
)

app.add_middleware(
    SessionMiddleware,
    secret_key="talentai-secret-key"
)

# =========================
# JINJA / I18N
# =========================

configure_jinja()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../templates")
)

STATIC_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../static")
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

Base.metadata.create_all(bind=engine)

# =========================
#  BANCO
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# =========================
#  REGISTER
# =========================
@app.get("/register", response_class=HTMLResponse)
def tela_register(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request
        }
    )

@app.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):

    usuario_existente = (
        db.query(Usuario)
        .filter(Usuario.email == email)
        .first()
    )

    if usuario_existente:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "erro": "Usuário já cadastrado"
            }
        )

    novo_usuario = Usuario(
        email=email,
        senha=senha
    )

    db.add(novo_usuario)
    db.commit()

    request.session["user_id"] = novo_usuario.id

    return RedirectResponse(
        url="/",
        status_code=302
    )

# =========================
#  LOGIN
# =========================
@app.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )

@app.post("/login")
def login(request: Request, email: str = Form(...), senha: str = Form(...), db=Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user or user.senha != senha:
        return templates.TemplateResponse(
    request=request,
    name="login.html",
    context={
        "request": request,
        "erro": "Email ou senha inválidos"
    }
)

    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=302)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

# =========================
#  LANGUAGE
# =========================

@app.get("/language/{language}")
def change_language(
    language: str,
    request: Request
):

    allowed_languages = {
        "pt-BR",
        "en-US"
    }

    if language not in allowed_languages:
        language = "pt-BR"

    request.session["language"] = language

    referer = request.headers.get("referer")

    return RedirectResponse(
        url=referer or "/",
        status_code=302
    )

# =========================
#  HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):

    print(" HOME CARREGANDO")

    try:
        vagas_ativas = (
            db.query(Vaga)
            .filter(Vaga.status == "Aberta")
            .all()
        )

        vagas_fechadas = (
            db.query(Vaga)
            .filter(Vaga.status == "Fechada")
            .all()
        )
    except Exception as e:
        print(" ERRO AO BUSCAR VAGAS:", e)
        vagas = []

    return templates.TemplateResponse(
    request=request,
    name="vagas.html",
    context={
        "request": request,
        "vagas_ativas": vagas_ativas,
        "vagas_fechadas": vagas_fechadas
    }
)
                
@app.post("/analisar_cvs/{vaga_id}")
async def analisar_cvs(
    vaga_id: int,
    arquivos: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):

    print("🚀 INICIO ANALISE")

    vaga = db.query(Vaga).filter(
        Vaga.id == vaga_id
    ).first()

    if not vaga:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    caminho_pasta = "uploads_cvs"
    os.makedirs(caminho_pasta, exist_ok=True)

    for arquivo in arquivos:

        try:

            print(f"📄 Processando: {arquivo.filename}")

            conteudo = await arquivo.read()

            nome_arquivo = arquivo.filename.replace(" ", "_")

            caminho_cv = os.path.join(
                caminho_pasta,
                nome_arquivo
            )

            with open(caminho_cv, "wb") as f:
                f.write(conteudo)

            candidato = processar_candidato(
                arquivo=arquivo,
                vaga=vaga,
                caminho_cv=caminho_cv,
                db=db
            )

            if candidato is None:
                continue

        except Exception as e:

            print("=" * 60)
            print(f"❌ Erro ao processar: {arquivo.filename}")
            print(e)
            print("=" * 60)

            continue

    db.commit()

    print("✅ ANALISE FINALIZADA")

    return RedirectResponse(
        url=f"/vaga/{vaga.id}",
        status_code=303
    )

@app.get("/health")
def health():
    return {"status": "ok"}


