from fastapi import (
    APIRouter,
    Request,
    Depends,
    UploadFile,
    File,
    Form
)

from fastapi.responses import (
    HTMLResponse,
    FileResponse,
    RedirectResponse
)

from app.core.templates import templates

from sqlalchemy.orm import Session

from app.db import SessionLocal

from app.models import (
    Candidato,
    Candidatura,
    Vaga,
    AnotacaoRecrutador
)

from app.services.cv_parser import extrair_texto_cv
from app.services.email_extractor import extrair_email
from app.services.phone_extractor import extrair_telefone
from app.services.ai_candidate_profile import gerar_perfil_profissional
from app.services.candidate_processor import (
    buscar_talento_unico_por_email,
    normalizar_email_identidade,
    processar_candidato
)
from datetime import datetime
from types import SimpleNamespace

import os
import tempfile
import urllib.parse
import re
import json

router = APIRouter()

@router.get("/teste")
def teste():
    return {"ok": True}


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
# BANCO DE TALENTOS
# =========================

@router.get(
    "/banco_talentos",
    response_class=HTMLResponse
)
def banco_talentos(
    request: Request,
    db: Session = Depends(get_db)
):

    candidatos = (
        db.query(Candidato)
        .order_by(Candidato.data_upload.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="banco_talentos.html",
        context={
            "request": request,
            "candidatos": candidatos
        }
    )

# =========================
# CONSULTOR 360
# =========================

@router.get(
    "/consultor/{candidato_id}",
    response_class=HTMLResponse
)
def consultor_360(
    candidato_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not candidato:
        return RedirectResponse(
            url="/banco_talentos",
            status_code=303
        )

    # =========================
    # SKILLS
    # =========================

    skills = []

    if candidato.skills_extraidas:
        skills = [
            skill.strip()
            for skill in candidato.skills_extraidas.split(",")
            if skill.strip()
        ]

    # =========================
    # CONSULTANT 360 — TALIA
    # =========================

    consultant360 = {}

    if candidato.dados_ia:

        try:

            dados_ia = json.loads(
                candidato.dados_ia
            )

            talia_data = dados_ia.get(
                "talia",
                {}
            ) or {}

            agents = talia_data.get(
                "agents",
                {}
            ) or {}

            consultant360_data = agents.get(
                "consultant360",
                {}
            ) or {}

            consultant360 = consultant360_data.get(
                "analysis",
                {}
            ) or {}

        except (
            json.JSONDecodeError,
            TypeError,
            AttributeError
        ):

            consultant360 = {}

    # =========================
    # CARREGAR ANOTAÇÕES
    # =========================

    anotacoes = (
        db.query(AnotacaoRecrutador)
        .filter(
            AnotacaoRecrutador.candidato_id == candidato_id
        )
        .order_by(
            AnotacaoRecrutador.data_criacao.desc()
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="consultor_360.html",
        context={
            "request": request,
            "candidato": candidato,
            "skills": skills,
            "consultant360": consultant360,
            "anotacoes": anotacoes
        }
    )

# =========================
# ANALISAR TALENTO PARA UMA VAGA
# =========================

@router.get(
    "/consultor/{candidato_id}/analisar-vaga",
    response_class=HTMLResponse
)
def analisar_talento_vaga(
    candidato_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not candidato:
        return RedirectResponse(
            url="/banco_talentos",
            status_code=303
        )

    vaga_ids_existentes = [
        item[0]
        for item in (
            db.query(Candidatura.vaga_id)
            .filter(Candidatura.candidato_id == candidato_id)
            .all()
        )
    ]

    query_vagas = (
        db.query(Vaga)
        .filter(Vaga.status == "Aberta")
    )

    if vaga_ids_existentes:
        query_vagas = query_vagas.filter(
            ~Vaga.id.in_(vaga_ids_existentes)
        )

    vagas = (
        query_vagas
        .order_by(Vaga.data_criacao.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="analisar_talento_vaga.html",
        context={
            "request": request,
            "candidato": candidato,
            "vagas": vagas
        }
    )


@router.post(
    "/consultor/{candidato_id}/analisar-vaga",
    response_class=HTMLResponse
)
def analisar_talento_vaga_submit(
    candidato_id: int,
    request: Request,
    vaga_id: int = Form(...),
    db: Session = Depends(get_db)
):

    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    vaga = (
        db.query(Vaga)
        .filter(
            Vaga.id == vaga_id,
            Vaga.status == "Aberta"
        )
        .first()
    )

    if not candidato or not vaga:
        return RedirectResponse(
            url="/banco_talentos",
            status_code=303
        )

    candidatura_existente = (
        db.query(Candidatura)
        .filter(
            Candidatura.candidato_id == candidato.id,
            Candidatura.vaga_id == vaga.id
        )
        .first()
    )

    if candidatura_existente:
        return RedirectResponse(
            url=f"/vaga/{vaga.id}",
            status_code=303
        )

    if not candidato.caminho_cv or not os.path.exists(candidato.caminho_cv):
        vagas = (
            db.query(Vaga)
            .filter(Vaga.status == "Aberta")
            .order_by(Vaga.data_criacao.desc())
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="analisar_talento_vaga.html",
            context={
                "request": request,
                "candidato": candidato,
                "vagas": vagas,
                "erro": "CV_NOT_FOUND"
            },
            status_code=400
        )

    arquivo_virtual = SimpleNamespace(
        filename=candidato.nome_arquivo or f"talento_{candidato.id}.pdf"
    )

    resultado = processar_candidato(
        arquivo=arquivo_virtual,
        vaga=vaga,
        caminho_cv=candidato.caminho_cv,
        db=db,
        origem="Banco de Talentos",
        email_confirmado=candidato.email,
        telefone_confirmado=candidato.telefone
    )

    if resultado is None:
        return RedirectResponse(
            url=f"/vaga/{vaga.id}",
            status_code=303
        )

    return RedirectResponse(
        url=f"/vaga/{vaga.id}",
        status_code=303
    )


# =========================
# NOVA ANOTAÇÃO
# =========================

@router.post("/nova_anotacao/{candidato_id}")
def nova_anotacao(
    candidato_id: int,
    request: Request,
    tipo: str = Form("Observação"),
    texto: str = Form(...),
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=302
        )

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not candidato:
        return RedirectResponse(
            url="/banco_talentos",
            status_code=303
        )

    anotacao = AnotacaoRecrutador(
        candidato_id=candidato.id,
        vaga_id=candidato.vaga_id,
        usuario_id=user_id,
        tipo=tipo,
        texto=texto
    )

    db.add(anotacao)

    candidato.ultimo_contato = datetime.utcnow()

    db.commit()

    return RedirectResponse(
        url=f"/consultor/{candidato.id}",
        status_code=303
    )

@router.get("/editar_comercial/{candidato_id}")
def editar_comercial(
    candidato_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    return templates.TemplateResponse(
        request=request,
        name="editar_comercial.html",
        context={
            "request": request,
            "candidato": candidato
        }
    )

@router.post("/editar_comercial/{candidato_id}")
def salvar_comercial(
    candidato_id: int,
    taxa_candidato: str = Form(""),
    disponibilidade: str = Form(""),
    cliente_atual: str = Form(""),
    projeto_atual: str = Form(""),
    modelo_trabalho: str = Form(""),
    modelo_contratacao: str = Form(""),
    db: Session = Depends(get_db)
):

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not candidato:
        return RedirectResponse("/", status_code=303)

    candidato.taxa_candidato = taxa_candidato
    candidato.disponibilidade = disponibilidade
    candidato.cliente_atual = cliente_atual
    candidato.projeto_atual = projeto_atual
    candidato.modelo_trabalho = modelo_trabalho
    candidato.modelo_contratacao = modelo_contratacao

    db.commit()

    return RedirectResponse(
        url=f"/consultor/{candidato_id}",
        status_code=303
    )

# =========================
# VISUALIZAR CV
# =========================

@router.get("/visualizar_cv/{candidato_id}")
def visualizar_cv(
    candidato_id: int,
    db: Session = Depends(get_db)
):

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not candidato:
        return {"erro": "Candidato não encontrado"}

    if not candidato.caminho_cv:
        return {"erro": "CV sem caminho salvo"}

    if not os.path.exists(candidato.caminho_cv):
        return {
            "erro": f"Arquivo não encontrado: {candidato.caminho_cv}"
        }

    return FileResponse(
        path=candidato.caminho_cv,
        filename=candidato.nome_arquivo,
        media_type="application/octet-stream"
    )
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

        termo = q.lower()

        for c in candidatos:

            texto = (c.texto_cv or "").lower()

            nome = (c.nome_arquivo or "").lower()

            if termo in texto or termo in nome:

                resultados.append({
                    "id": c.id,
                    "nome": c.nome_arquivo,
                    "match": int(c.score or 0),
                    "skills_ok": (
                        (c.skills_extraidas or "").split(",")
                        if c.skills_extraidas else []
                    ),
                    "skills_faltantes": (
                        (c.skills_faltantes or "").split(",")
                        if c.skills_faltantes else []
                    )
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

# =========================
#  WHATSAPP CANDIDATO
# =========================

@router.get("/whatsapp_candidato/{vaga_id}/{candidato_id}")
def whatsapp_candidato(
    vaga_id: int,
    candidato_id: int,
    db: Session = Depends(get_db)
):

    vaga = (
        db.query(Vaga)
        .filter(Vaga.id == vaga_id)
        .first()
    )

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not vaga or not candidato:
        return {"erro": "Dados não encontrados"}

    telefone = candidato.telefone or ""

    telefone = re.sub(r"\D", "", telefone)

    if telefone.startswith("0"):
        telefone = telefone[1:]

    if not telefone.startswith("55"):
        telefone = "55" + telefone

    mensagem = f"""
Olá {candidato.nome_arquivo.split('.')[0]}, tudo bem?

Seu perfil apresentou aderência para a oportunidade:

Vaga: {vaga.titulo}

Gostaria de conversar com você sobre os próximos passos.

Att,
TalentAI
AI-Powered Talent Intelligence
"""

    mensagem = urllib.parse.quote(mensagem)

    link = f"https://wa.me/{telefone}?text={mensagem}"

    return RedirectResponse(
        url=link,
        status_code=302
    )

# =========================
#  UPLOAD BANCO DE TALENTOS
# =========================
@router.post("/upload_cv_banco")
async def upload_cv_banco(
    request: Request,
    cvs: list[UploadFile] = File(...),
    idioma: str = Form("PT"),
    db: Session = Depends(get_db)
):

    print(" UPLOAD BANCO TALENTOS")

    for arquivo in cvs:

        try:
            print(f"📄 Processando: {arquivo.filename}")

            conteudo = await arquivo.read()
            # =========================
            #  SALVAR CV FISICAMENTE
            # =========================
            nome_arquivo = arquivo.filename.replace(" ", "_")

            caminho_pasta = "uploads"

            os.makedirs(caminho_pasta, exist_ok=True)

            caminho_cv = os.path.join(
              caminho_pasta,
              nome_arquivo
            )

            with open(caminho_cv, "wb") as f:
               f.write(conteudo)

            # salva temporário
            sufixo = os.path.splitext(arquivo.filename)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=sufixo
            ) as tmp:

                tmp.write(conteudo)
                caminho_temp = tmp.name

            # extrair texto
            texto = extrair_texto_cv(caminho_temp) or ""

            # =============================================
            # TALENT PROFILE — LEITURA INTELIGENTE DO CV
            # =============================================

            perfil = gerar_perfil_profissional(texto) or {}

            # contato
            email_extraido = extrair_email(texto)
            email = (
                normalizar_email_identidade(email_extraido)
                or email_extraido
            )
            telefone = extrair_telefone(texto)

            # =============================================
            # TALENT BANK 2.0 — FIND OR CREATE DO TALENTO
            # =============================================

            candidato = buscar_talento_unico_por_email(
                db,
                email
            )

            if candidato is not None:

                candidato.nome_arquivo = arquivo.filename
                candidato.caminho_cv = caminho_cv
                candidato.texto_cv = texto
                candidato.email = email
                candidato.telefone = telefone
                candidato.idioma = idioma

                # Atualiza os dados permanentes do Talent Profile
                # com a leitura mais recente do CV, sem executar match.
                candidato.resumo = perfil.get("resumo", "") or candidato.resumo
                candidato.titulo_profissional = (
                    perfil.get("titulo_profissional", "")
                    or candidato.titulo_profissional
                )
                candidato.anos_experiencia = (
                    perfil.get("anos_experiencia", "")
                    or candidato.anos_experiencia
                )
                candidato.localizacao = (
                    perfil.get("localizacao", "")
                    or candidato.localizacao
                )
                candidato.idiomas = (
                    perfil.get("idiomas", "")
                    or candidato.idiomas
                )
                candidato.setores = (
                    perfil.get("setores", "")
                    or candidato.setores
                )

                print(
                    "♻️ Talento existente atualizado no banco:",
                    candidato.id
                )

            else:

                candidato = Candidato(
                    nome_arquivo=arquivo.filename,
                    caminho_cv=caminho_cv,
                    texto_cv=texto,
                    email=email,
                    telefone=telefone,
                    score=0,
                    resumo=perfil.get("resumo", ""),
                    titulo_profissional=perfil.get(
                        "titulo_profissional",
                        ""
                    ),
                    anos_experiencia=perfil.get(
                        "anos_experiencia",
                        ""
                    ),
                    localizacao=perfil.get(
                        "localizacao",
                        ""
                    ),
                    idiomas=perfil.get(
                        "idiomas",
                        ""
                    ),
                    setores=perfil.get(
                        "setores",
                        ""
                    ),
                    skills_extraidas="",
                    skills_faltantes="",
                    vaga_id=None,
                    origem="Banco de Talentos",
                    idioma=idioma
                )

                db.add(candidato)

                print(
                    "✅ Novo talento adicionado ao banco:",
                    arquivo.filename
                )

        except Exception as e:

            print("❌ ERRO CV BANCO:")
            print(e)

            continue

    db.commit()

    print(" BANCO TALENTOS FINALIZADO")

    return RedirectResponse(
        url="/banco_talentos",
        status_code=303
    )

# =========================
# ALTERAR ETAPA
# =========================

@router.post("/alterar_etapa/{candidato_id}")
def alterar_etapa(
    candidato_id: int,
    etapa: str = Form(...),
    db: Session = Depends(get_db)
):

    print("==========")
    print("CANDIDATO:", candidato_id)
    print("ETAPA RECEBIDA:", etapa)
    print("==========")

    candidato = (
        db.query(Candidato)
        .filter(Candidato.id == candidato_id)
        .first()
    )

    if not candidato:
        return {"erro": "Candidato não encontrado"}

    candidato.etapa = etapa

    print("ANTES COMMIT:", candidato.etapa)

    db.commit()

    db.refresh(candidato)

    print("DEPOIS COMMIT:", candidato.etapa)

    return RedirectResponse(
        url=f"/vaga/{candidato.vaga_id}",
        status_code=303
)
