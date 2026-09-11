import json

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Vaga, Candidato, Candidatura
from app.core.templates import templates

from app.services.cv_parser import extrair_texto_cv
from app.services.match import calcular_match
from app.services.ai_candidate_profile import gerar_perfil_profissional
from app.services.experience_extractor import extrair_historico_profissional
from app.intelligence.talia.talia import Talia
from app.intelligence.context.analysis_context import AnalysisContext

from dataclasses import asdict, is_dataclass
from enum import Enum


router = APIRouter()
talia = Talia()


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
# JSON SERIALIZATION
# =========================

def _serializar_para_json(obj):

    if is_dataclass(obj):
        return asdict(obj)

    if isinstance(obj, Enum):
        return obj.value

    if hasattr(obj, "isoformat"):

        try:
            return obj.isoformat()

        except Exception:
            pass

    if isinstance(obj, set):
        return list(obj)

    return str(obj)


# =========================
# DETALHE VAGA
# =========================

@router.get("/vaga/{vaga_id}")
def detalhe_vaga(
    request: Request,
    vaga_id: int,
    db: Session = Depends(get_db)
):

    print("🔥 ABRINDO DETALHE DA VAGA")

    try:

        vaga = (
            db.query(Vaga)
            .filter(Vaga.id == vaga_id)
            .first()
        )

        print("✅ VAGA OK")

        if not vaga:

            return HTMLResponse(
                "Vaga não encontrada",
                status_code=404
            )

        resultados = (
            db.query(
                Candidato,
                Candidatura
            )
            .join(
                Candidatura,
                Candidatura.candidato_id == Candidato.id
            )
            .filter(
                Candidatura.vaga_id == vaga_id
            )
            .order_by(
                Candidatura.match_score.desc()
            )
            .all()
        )

        candidatos = []

        for candidato, candidatura in resultados:

            if candidatura.match_score is not None:
                candidato.score = float(candidatura.match_score)

            if candidatura.match_data:

                try:

                    dados_candidatura = json.loads(
                        candidatura.match_data
                    )

                    perfil = dados_candidatura.get(
                        "perfil",
                        {}
                    )

                    match = dados_candidatura.get(
                        "match",
                        {}
                    )

                    if isinstance(perfil, dict):

                        resumo = perfil.get("resumo")

                        if resumo is not None:
                            candidato.resumo = resumo

                    if isinstance(match, dict):

                        encontradas = match.get(
                            "encontradas",
                            []
                        )

                        faltantes = match.get(
                            "faltantes",
                            []
                        )

                        if isinstance(encontradas, list):

                            candidato.skills_extraidas = ", ".join(
                                str(item)
                                for item in encontradas
                            )

                        elif encontradas is not None:

                            candidato.skills_extraidas = str(
                                encontradas
                            )

                        if isinstance(faltantes, list):

                            candidato.skills_faltantes = ", ".join(
                                str(item)
                                for item in faltantes
                            )

                        elif faltantes is not None:

                            candidato.skills_faltantes = str(
                                faltantes
                            )

                    candidato.dados_ia = candidatura.match_data

                except (
                    json.JSONDecodeError,
                    TypeError
                ) as e:

                    print(
                        "⚠️ MATCH_DATA INVÁLIDO:",
                        candidatura.id,
                        e
                    )

            candidatos.append(candidato)

        print(
            "✅ CANDIDATURAS OK:",
            len(candidatos)
        )

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

        print(
            "❌ ERRO DETALHE VAGA:",
            e
        )

        return HTMLResponse(
            "Erro ao carregar detalhe da vaga",
            status_code=500
        )


# =====================================================
# REANALISAR TALENTO × VAGA COM TALIA
# =====================================================

@router.post("/vaga/{vaga_id}/candidato/{candidato_id}/reanalisar")
def reanalisar_talento_vaga(
    vaga_id: int,
    candidato_id: int,
    db: Session = Depends(get_db)
):

    print("=" * 80)
    print("🔄 REANÁLISE TALIA")
    print("CANDIDATO:", candidato_id)
    print("VAGA:", vaga_id)
    print("=" * 80)

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

    candidatura = (
        db.query(Candidatura)
        .filter(
            Candidatura.candidato_id == candidato_id,
            Candidatura.vaga_id == vaga_id
        )
        .first()
    )

    if not vaga or not candidato or not candidatura:

        return HTMLResponse(
            "Vaga, talento ou candidatura não encontrada.",
            status_code=404
        )

    if not candidato.caminho_cv:

        return HTMLResponse(
            "O talento não possui CV armazenado.",
            status_code=400
        )

    try:

        texto = extrair_texto_cv(
            candidato.caminho_cv
        ) or candidato.texto_cv or ""

        if not texto.strip():

            return HTMLResponse(
                "Não foi possível extrair texto do CV.",
                status_code=400
            )

        historico_profissional = (
            extrair_historico_profissional(
                texto
            )
        )

        perfil = gerar_perfil_profissional(
            texto
        ) or {}

        resultado_match = calcular_match(
            vaga,
            texto
        )

        context = AnalysisContext(
            texto_cv=texto,
            perfil=perfil,
            match=resultado_match,
            historico_profissional=historico_profissional
        )

        analise_talia = talia.analisar_candidato(
            candidato=candidato,
            vaga=vaga,
            context=context
        )

        # =====================================================
        # MATCH PERSISTIDO
        # =====================================================
        #
        # resultado_match é o matcher legado usado como contexto
        # de compatibilidade durante a execução da TALIA.
        #
        # Para a Candidatura e para a tela da vaga, porém, a fonte
        # oficial de skills deve ser o MatchResult produzido pela
        # TALIA. Isso evita que palavras-chave literais da vaga
        # (por exemplo, um título/função profissional) reapareçam
        # como skills faltantes depois que a TALIA já classificou
        # semanticamente os requisitos reais da demanda.
        #
        # Se por algum motivo o MatchResult oficial não estiver
        # disponível, preservamos o resultado legado como fallback.
        # =====================================================

        match_persistido = resultado_match

        analysis_result = analise_talia.get(
            "decision"
        )

        if isinstance(analysis_result, dict):

            decision = analysis_result.get(
                "decision"
            )

        else:

            decision = analysis_result

        if decision is not None:

            overall_match = getattr(
                decision,
                "overall_match",
                None
            )

            if overall_match is not None:

                candidato.score = float(
                    overall_match
                )

            match_result = getattr(
                decision,
                "match_result",
                None
            )

            if match_result is not None:

                matched_skills = getattr(
                    match_result,
                    "matched_skills",
                    {}
                ) or {}

                missing_skills = getattr(
                    match_result,
                    "missing_skills",
                    {}
                ) or {}

                skills_encontradas = []
                skills_faltantes = []

                for categoria in (
                    "mandatory",
                    "unclassified",
                    "nice_to_have"
                ):

                    skills_encontradas.extend(
                        matched_skills.get(
                            categoria,
                            []
                        )
                    )

                for categoria in (
                    "mandatory",
                    "unclassified"
                ):

                    skills_faltantes.extend(
                        missing_skills.get(
                            categoria,
                            []
                        )
                    )

                skills_encontradas = list(
                    dict.fromkeys(
                        skills_encontradas
                    )
                )

                skills_faltantes = list(
                    dict.fromkeys(
                        skills_faltantes
                    )
                )

                candidato.skills_extraidas = ", ".join(
                    skills_encontradas
                )

                candidato.skills_faltantes = ", ".join(
                    skills_faltantes
                )

                # =============================================
                # SNAPSHOT OFICIAL DE SKILLS DA CANDIDATURA
                # =============================================
                #
                # A chave "match" é consumida pela tela da vaga.
                # A partir daqui ela passa a representar as skills
                # oficiais do MatchResult da TALIA, e não o matcher
                # literal legado.
                # =============================================

                match_persistido = {
                    "encontradas": skills_encontradas,
                    "faltantes": skills_faltantes
                }

        # O perfil é do talento e pode ser atualizado
        # com a leitura atual do CV.
        candidato.texto_cv = texto
        candidato.resumo = perfil.get(
            "resumo",
            candidato.resumo or ""
        )
        candidato.titulo_profissional = perfil.get(
            "titulo_profissional",
            candidato.titulo_profissional or ""
        )
        candidato.anos_experiencia = perfil.get(
            "anos_experiencia",
            candidato.anos_experiencia or ""
        )
        candidato.localizacao = perfil.get(
            "localizacao",
            candidato.localizacao or ""
        )
        candidato.idiomas = perfil.get(
            "idiomas",
            candidato.idiomas or ""
        )
        candidato.setores = perfil.get(
            "setores",
            candidato.setores or ""
        )

        relatorio_ia = {
            "perfil": perfil,
            "match": match_persistido,
            "match_legado": resultado_match,
            "talia": analise_talia
        }

        dados_ia = json.dumps(
            relatorio_ia,
            ensure_ascii=False,
            default=_serializar_para_json
        )

        # Compatibilidade temporária com telas legadas.
        candidato.dados_ia = dados_ia

        # A verdade do match desta vaga fica na candidatura.
        candidatura.match_score = (
            int(round(float(candidato.score)))
            if candidato.score is not None
            else None
        )

        candidatura.match_data = dados_ia

        db.commit()

        db.refresh(candidato)
        db.refresh(candidatura)

        print(
            "✅ REANÁLISE TALIA CONCLUÍDA:",
            "candidato",
            candidato.id,
            "| vaga",
            vaga.id,
            "| candidatura",
            candidatura.id,
            "| match",
            candidatura.match_score
        )

        return RedirectResponse(
            url=f"/vaga/{vaga_id}",
            status_code=303
        )

    except Exception as e:

        db.rollback()

        print(
            "❌ ERRO REANÁLISE TALIA:",
            e
        )

        return HTMLResponse(
            "Erro ao reanalisar talento com TALIA.",
            status_code=500
        )
