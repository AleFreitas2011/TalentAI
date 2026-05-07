from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from typing import List

import tempfile
import json
import urllib.parse
import re

from .db import SessionLocal, engine, Base
from .models import Vaga, Usuario, Cliente, Candidato, Envio
import os

from app.services.cv_parser import extrair_texto_cv
from app.services.email_extractor import extrair_email
from app.services.phone_extractor import extrair_telefone
from app.services.match import calcular_match
from app.services.ai_match import analisar_cv_com_ia
from app.services.email_sender import enviar_email

print("🔥 CODIGO NOVO RODANDO 🔥")

# =========================
# 🚀 APP
# =========================
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="talentai-secret-key")

from fastapi.staticfiles import StaticFiles
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../templates")
)

STATIC_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../static")
)

templates = Jinja2Templates(directory=TEMPLATES_DIR)
 
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

Base.metadata.create_all(bind=engine)

# =========================
# 🔥 BANCO
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# 🔐 LOGIN
# =========================
@app.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, email: str = Form(...), senha: str = Form(...), db=Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user or user.senha != senha:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "erro": "Email ou senha inválidos"
        })

    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=302)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

# =========================
# 🏠 HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):

    print("🔥 HOME CARREGANDO")

    try:
        vagas = db.query(Vaga).all()
    except Exception as e:
        print("❌ ERRO AO BUSCAR VAGAS:", e)
        vagas = []

    return templates.TemplateResponse(
        name="vagas.html",
        request=request,
        context={
            "vagas": vagas
        }
    )
    

@app.get("/nova_vaga", response_class=HTMLResponse)
def tela_nova_vaga(request: Request, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()

    return templates.TemplateResponse("nova_vaga.html", {
        "request": request,
        "clientes": clientes
    })

@app.post("/nova_vaga")
def nova_vaga(
    request: Request,
    titulo: str = Form(...),
    cliente_id: int = Form(...),
    descricao: str = Form(""),
    palavras_chave: str = Form(""),
    status: str = Form("Aberta"),
    db=Depends(get_db)
):
    if not request.session.get("user_id"):
        return RedirectResponse("/login", status_code=302)

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
    return RedirectResponse("/", status_code=303)

@app.get("/vaga/{vaga_id}")
def detalhe_vaga(
    request: Request,
    vaga_id: int,
    db: Session = Depends(get_db)
):
    print("🔥 ABRINDO DETALHE DA VAGA")

    try:
        vaga = db.query(Vaga).filter(Vaga.id == vaga_id).first()

        print("✅ VAGA OK")

        if not vaga:
            return HTMLResponse(
                "Vaga não encontrada",
                status_code=404
            )

        candidatos = (
            db.query(Candidato)
            .filter(Candidato.vaga_id == vaga_id)
            .order_by(Candidato.score.desc())
            .all()
        )

        print("✅ CANDIDATOS OK")

        for c in candidatos:
            print("👤", c.nome_arquivo, c.score)

        return templates.TemplateResponse(
            request=request,
            name="vaga_detalhe.html",
            context={
                "request": request,
                "vaga": vaga,
                "candidatos": candidatos
            }
        )

    except Exception as e:
        print("❌ ERRO DETALHE VAGA:")
        print(e)

        return HTMLResponse(
            f"ERRO DETALHE VAGA: {str(e)}",
            status_code=500
        )
        
# =========================
# 🤖 ANALISAR CVS (ROTA FINAL LIMPA)
# =========================
@app.post("/analisar_cvs/{vaga_id}")
async def analisar_cvs(
    vaga_id: int,
    arquivos: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    import tempfile
    import json

    print("🚀 INICIO ANALISE")

    vaga = db.query(Vaga).filter(Vaga.id == vaga_id).first()

    if not vaga:
        return RedirectResponse(url="/", status_code=303)

    for arquivo in arquivos:
        try:
            print(f"📄 Processando: {arquivo.filename}")

            conteudo = await arquivo.read()

            # salvar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(conteudo)
                caminho_temp = tmp.name

            texto = extrair_texto_cv(caminho_temp) or ""

            # 📧 CONTATO
            email = extrair_email(texto)
            telefone = extrair_telefone(texto)

            # 🧠 MATCH
            resultado_match = calcular_match(vaga, texto)

            try:
                if isinstance(resultado_match, dict):
                    score_regra = len(resultado_match.get("encontradas", [])) * 10
                else:
                    score_regra = float(resultado_match)
            except:
                score_regra = 10

            # 🤖 RESUMO COM IA
            try:
                resultado_ia = analisar_cv_com_ia(texto, vaga.descricao)

                if isinstance(resultado_ia, dict):
                    resumo_ia = resultado_ia.get("resumo", "Resumo não gerado")
                else:
                    resumo_ia = "Resumo não gerado"

            except Exception as e:
                print("⚠️ ERRO NA IA:", e)

                # 🔥 FALLBACK INTELIGENTE (NUNCA QUEBRA UX)
                if texto:
                  resumo_ia = texto[:300]
                else:
                  resumo_ia = "Resumo não disponível"

            # 🔥 NORMALIZA SCORE
            score_final = max(0, min(score_regra, 100))
            
            # 🔒 EVITA DUPLICAÇÃO
            existe = db.query(Candidato).filter(
                Candidato.nome_arquivo == arquivo.filename,
                Candidato.vaga_id == vaga.id
            ).first()

            if existe:
              print(f"⚠️ CV já existe, ignorando: {arquivo.filename}")
              continue

            # 💾 SALVAR
            candidato = Candidato(
                nome_arquivo=arquivo.filename,
                texto_cv=texto,
                email=email,
                telefone=telefone,
                score=score_final,
                resumo=resumo_ia,
                dados_ia=json.dumps(resultado_match) if isinstance(resultado_match, dict) else None,
                vaga_id=vaga.id,

                # 🔥 NOVO CAMPO AQUI
                origem="Upload CV"
            )

            db.add(candidato)

        except Exception as e:
            print("❌ ERRO NO CV:", arquivo.filename)
            print(e)
            continue

    db.commit()

    print("✅ ANALISE FINALIZADA")

    return RedirectResponse(url=f"/vaga/{vaga.id}", status_code=303)
#=========================
# 📲 WHATSAPP
# =========================
@app.get("/whatsapp_candidato/{vaga_id}/{candidato_id}")
def whatsapp_candidato(vaga_id: int, candidato_id: int, db: Session = Depends(get_db)):
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    vaga = db.query(Vaga).filter(Vaga.id == vaga_id).first()

    if not candidato or not candidato.telefone:
        return RedirectResponse(f"/vaga/{vaga_id}", status_code=303)

    telefone = re.sub(r"\D", "", candidato.telefone)

    if not telefone.startswith("55"):
        telefone = "55" + telefone

    mensagem = urllib.parse.quote(f"""
Olá, tudo bem?

Vi seu perfil e gostaria de falar sobre a vaga:

💼 {vaga.titulo}

Podemos conversar?
""")

    return RedirectResponse(f"https://wa.me/{telefone}?text={mensagem}", status_code=302)

 
# =========================
# 📧 ENVIAR CLIENTE
# =========================
@app.post("/enviar_cliente/{vaga_id}")
def enviar_cliente(
    vaga_id: int,
    request: Request,
    candidatos_ids: List[int] = Form(default=[]),
    cliente_id: int = Form(...),
    idioma: str = Form("PT"),
    db: Session = Depends(get_db)
):
    print("🚀 INICIANDO ENVIO")

    try:
        if not candidatos_ids:
            return RedirectResponse(url=f"/vaga/{vaga_id}", status_code=303)

        vaga = db.query(Vaga).filter(Vaga.id == vaga_id).first()
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not vaga or not cliente:
            return RedirectResponse(url=f"/vaga/{vaga_id}", status_code=303)

        candidatos = db.query(Candidato).filter(
            Candidato.id.in_(candidatos_ids)
        ).all()

        conteudo_email = ""

        # 🔹 CABEÇALHO
        if idioma == "EN":
            conteudo_email += f"""Hi {cliente.nome_contato.split()[0] if cliente.nome_contato else "Client"},

Please find below the candidates for the position: {vaga.titulo}
"""
        else:
            conteudo_email += f"""Olá {cliente.nome_contato.split()[0] if cliente.nome_contato else "Cliente"},

Segue abaixo os candidatos para a vaga: {vaga.titulo}
"""

        # 🔹 CANDIDATOS
        for c in candidatos:
            c.etapa = "Enviado"

            if idioma == "EN":
                conteudo_email += f"""

Candidate: {c.nome_arquivo}
Match Score: {c.score or 0}%

Summary:
{c.resumo or "No summary"}

Email: {c.email or "-"}
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

        # 🔹 FINAL
        if idioma == "EN":
            conteudo_email += "\n\nHappy to discuss next steps."
        else:
            conteudo_email += "\n\nFico à disposição para próximos passos."

        import urllib.parse

        link = f"https://mail.google.com/mail/?view=cm&fs=1&to={cliente.email}&su={urllib.parse.quote('Candidatos - ' + vaga.titulo)}&body={urllib.parse.quote(conteudo_email)}"

        print("🚀 LINK EMAIL:", link)

        return RedirectResponse(link, status_code=302)

        # 📊 SALVAR HISTÓRICO
        envio = Envio(
            vaga_id=vaga_id,
            cliente_id=cliente_id,
            candidatos=", ".join([c.nome_arquivo for c in candidatos])
        )

        db.add(envio)
        db.commit()

        return RedirectResponse(url=f"/vaga/{vaga_id}?sucesso=1", status_code=303)

         
        conteudo_email = ""

        # 🔹 CABEÇALHO
        if idioma == "EN":
            conteudo_email += f"""Hi {cliente.nome_contato.split()[0] if cliente.nome_contato else "Client"},

Please find below the candidates for the position: {vaga.titulo}
"""
        else:
            conteudo_email += f"""Olá {cliente.nome_contato.split()[0] if cliente.nome_contato else "Cliente"},

Segue abaixo os candidatos para a vaga: {vaga.titulo}
"""

        # 🔹 CANDIDATOS
        for c in candidatos:
            c.etapa = "Enviado"

            if idioma == "EN":
                conteudo_email += f"""

Candidate: {c.nome_arquivo}
Match Score: {c.score or 0}%

Summary:
{c.resumo or "No summary"}

Email: {c.email or "-"}
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

        # 🔹 FINAL
        if idioma == "EN":
            conteudo_email += "\n\nHappy to discuss next steps."
        else:
            conteudo_email += "\n\nFico à disposição para próximos passos."

        import urllib.parse

        link = f"https://mail.google.com/mail/?view=cm&fs=1&to={cliente.email}&su={urllib.parse.quote('Candidatos - ' + vaga.titulo)}&body={urllib.parse.quote(conteudo_email)}"

        print("🚀 LINK EMAIL:", link)

        return RedirectResponse(link, status_code=302)

        # 📊 CONTADOR
        if not hasattr(vaga, "candidatos_enviados") or vaga.candidatos_enviados is None:
            vaga.candidatos_enviados = 0

        vaga.candidatos_enviados += len(candidatos)

        envio = Envio(
            vaga_id=vaga_id,
            cliente_id=cliente_id,
            candidatos=", ".join([c.nome_arquivo for c in candidatos])
        )

        db.add(envio)
        db.commit()

        return RedirectResponse(url=f"/vaga/{vaga_id}?sucesso=1", status_code=303)

    except Exception as e:
        print("❌ ERRO NO ENVIO:", e)
        return RedirectResponse(url=f"/vaga/{vaga_id}", status_code=303)
    
    candidatos = db.query(Candidato).filter(
        Candidato.id.in_(candidatos_ids)
    ).all()

    lista_candidatos = []

    for c in candidatos:
        resumo_final = c.resumo or "Sem resumo"

        if idioma == "EN":
            try:
                from app.ai.client import client

                prompt = f"Translate this professional CV summary to English:\n\n{resumo_final}"

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                resumo_final = response.choices[0].message.content

            except Exception as e:
                print("⚠️ erro tradução:", e)

        if idioma == "PT":
            bloco = f"""
Candidato: {c.nome_arquivo}
Aderência: {c.score or 0}%

Resumo:
{resumo_final}

Email: {c.email or "-"}
Telefone: {c.telefone or "-"}
"""
        else:
            bloco = f"""
Candidate: {c.nome_arquivo}
Match Score: {c.score or 0}%

Summary:
{resumo_final}

Email: {c.email or "-"}
Phone: {c.telefone or "-"}
"""

        lista_candidatos.append(bloco)

    if idioma == "PT":
        conteudo_email = f"""
Olá {cliente.nome_contato.split()[0] if cliente.nome_contato else "Cliente"},

Segue abaixo os candidatos para a vaga: {vaga.titulo}

{"".join(lista_candidatos)}

Fico à disposição para próximos passos.
"""
    else:
        conteudo_email = f"""
Hi {cliente.nome_contato.split()[0] if cliente.nome_contato else "Client"},

Please find below shortlisted candidates for the position: {vaga.titulo}

{"".join(lista_candidatos)}

Happy to discuss next steps.
"""

    return templates.TemplateResponse(
        "email_preview.html",
        {
            "request": request,
            "vaga": vaga,
            "cliente": cliente,
            "email": conteudo_email
        }
    )
    
    # =========================
# 🏢 NOVO CLIENTE (TELA)
# =========================
@app.get("/novo_cliente", response_class=HTMLResponse)
def tela_novo_cliente(request: Request):
    return templates.TemplateResponse("novo_cliente.html", {"request": request})

# =========================
# 🏢 NOVO CLIENTE (SALVAR)
# =========================
@app.post("/novo_cliente")
def criar_cliente(
    request: Request,
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

    return RedirectResponse(url="/nova_vaga", status_code=303)

# =========================
# 📊 DASHBOARD
# =========================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    try:
        vagas_abertas = db.query(Vaga)\
            .filter(Vaga.status == "Aberta")\
            .count()

        total_candidatos = db.query(Candidato).count()

        media_score = db.query(Candidato.score).all()

        media = 0

        if media_score:
            media = round(
                sum([c[0] or 0 for c in media_score]) / len(media_score),
                2
            )

        print("✅ DASHBOARD OK")

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "request": request,
                "vagas_abertas": vagas_abertas,
                "total_candidatos": total_candidatos,
                "media_score": media
            }
        )

    except Exception as e:
        print("❌ ERRO DASHBOARD:")
        print(e)

        return HTMLResponse(
            f"ERRO DASHBOARD: {str(e)}",
            status_code=500
        )
    
# =========================
# 🧠 BANCO DE TALENTOS
# =========================
@app.get("/banco_talentos", response_class=HTMLResponse)
def banco_talentos(request: Request, db: Session = Depends(get_db)):

    candidatos = db.query(Candidato).order_by(Candidato.data_upload.desc()).all()

    return templates.TemplateResponse("banco_talentos.html", {
        "request": request,
        "candidatos": candidatos
    })
    
@app.get("/buscar_talentos", response_class=HTMLResponse)
def buscar_talentos(request: Request, q: str = "", db: Session = Depends(get_db)):

    candidatos = db.query(Candidato).all()

    resultados = []

    if q:
        termo = q.lower()

        for c in candidatos:
            texto = (c.texto_cv or "").lower()
            nome = (c.nome_arquivo or "").lower()

            if termo in texto or termo in nome:
                resultados.append({
                    "nome": c.nome_arquivo,
                    "match": int(c.score or 0),
                    "skills_ok": (c.skills_extraidas or "").split(",") if c.skills_extraidas else [],
                    "skills_faltantes": (c.skills_faltantes or "").split(",") if c.skills_faltantes else []
                })

    return templates.TemplateResponse("buscar_talentos.html", {
        "request": request,
        "resultados": resultados,
        "q": q
    })
    
@app.get("/health")
def health():
    return {"status": "ok"}