import json
import re

from dataclasses import asdict, is_dataclass

from enum import Enum

from app.models import Candidato, Candidatura

from app.services.cv_parser import extrair_texto_cv
from app.services.email_extractor import extrair_email
from app.services.phone_extractor import extrair_telefone
from app.services.match import calcular_match
from app.services.ai_candidate_profile import gerar_perfil_profissional
from app.intelligence.talia.talia import Talia
from app.services.experience_extractor import extrair_historico_profissional


# =========================
# TALIA
# =========================

talia = Talia()


# =====================================================
# JSON SERIALIZATION
# =====================================================

def _serializar_para_json(obj):
    """
    Converte objetos internos da TALIA para estruturas
    compatíveis com JSON.

    Mantém os objetos Decision/MatchResult intactos
    durante o processamento da TALIA.

    A conversão acontece somente no momento de
    persistir dados_ia.
    """

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



def normalizar_email_identidade(email):
    """Normaliza um e-mail utilizável como identidade segura do talento."""
    if not email:
        return None

    valor = str(email).strip().lower()

    if valor in {
        "não encontrado",
        "nao encontrado",
        "nÃ£o encontrado",
        "none",
        "null",
        ""
    }:
        return None

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valor):
        return None

    return valor


def buscar_talento_unico_por_email(db, email):
    """
    Reutiliza o talento somente quando a identidade é inequívoca.

    Duplicidades históricas não são mescladas automaticamente.
    """
    email_normalizado = normalizar_email_identidade(email)

    if not email_normalizado:
        return None

    candidatos = (
        db.query(Candidato)
        .filter(Candidato.email == email_normalizado)
        .order_by(Candidato.id.asc())
        .all()
    )

    if len(candidatos) == 1:
        return candidatos[0]

    if len(candidatos) > 1:
        print(
            "⚠️ Identidade histórica ambígua para e-mail:",
            email_normalizado,
            "| registros:",
            [c.id for c in candidatos]
        )

    return None

def processar_candidato(
    arquivo,
    vaga,
    caminho_cv,
    db,
    origem="Upload CV",
    email_confirmado=None,
    telefone_confirmado=None
):
    """
    Processa um currículo completo.

    Fluxo:

    Upload
        ↓
    Extração de texto
        ↓
    Extração de contatos
        ↓
    Perfil Executivo IA
        ↓
    Match legado
        ↓
    Salvar candidato
        ↓
    Criar candidatura
        ↓
    TALIA
        ↓
    Overall Match TALIA
        ↓
    Persistência do score oficial
        ↓
    Persistência do match na candidatura
    """

    # =========================
    # EXTRAIR TEXTO
    # =========================

    texto = extrair_texto_cv(caminho_cv) or ""

    historico_profissional = extrair_historico_profissional(
        texto
    )

    if not texto.strip():

        print(
            "❌ Não foi possível extrair texto."
        )

        return None

    # =========================
    # CONTATOS
    # =========================

    email_extraido = extrair_email(texto)

    email = (
        normalizar_email_identidade(email_confirmado)
        or normalizar_email_identidade(email_extraido)
        or email_extraido
    )

    print("=" * 80)
    print("TEXTO DO CV")
    print("=" * 80)
    print(texto[:1200])
    print("=" * 80)

    telefone_extraido = extrair_telefone(texto)

    telefone = (
        telefone_confirmado.strip()
        if telefone_confirmado and telefone_confirmado.strip()
        else telefone_extraido
    )

    print(
        "TELEFONE EXTRAÍDO:",
        telefone
    )

    # =========================
    # IA
    # =========================

    perfil = gerar_perfil_profissional(
        texto
    )

    if perfil is None:

        perfil = {}

    # =========================
    # MATCH LEGADO
    # =========================

    print("=" * 70)
    print("VAGA RECEBIDA PELO MATCH")
    print(
        "ID:",
        vaga.id
    )

    print(
        "Título:",
        vaga.titulo
    )

    print("Palavras-chave:")

    print(
        vaga.palavras_chave
    )

    print("=" * 70)

    resultado_match = calcular_match(
        vaga,
        texto
    )

    if isinstance(
        resultado_match,
        dict
    ):

        score = len(
            resultado_match.get(
                "encontradas",
                []
            )
        ) * 10

    else:

        try:

            score = float(
                resultado_match
            )

        except Exception:

            score = 0

    score = min(
        score,
        100
    )

    # =========================
    # TALENT BANK 2.0
    # FIND OR CREATE DO TALENTO
    # =========================

    candidato = buscar_talento_unico_por_email(
        db,
        email
    )

    if candidato is not None:

        candidatura_existente = (
            db.query(Candidatura)
            .filter(
                Candidatura.candidato_id == candidato.id,
                Candidatura.vaga_id == vaga.id
            )
            .first()
        )

        if candidatura_existente:
            print(
                "⚠️ Talento já possui candidatura para esta vaga:",
                candidato.id,
                "| vaga:",
                vaga.id
            )
            return None

        # O talento já existe. Atualizamos o cadastro permanente
        # com o CV/contatos mais recentes, sem alterar sua vaga
        # legada original. O histórico específico de cada vaga
        # permanece preservado em Candidatura.match_data.
        candidato.nome_arquivo = arquivo.filename
        candidato.caminho_cv = caminho_cv
        candidato.texto_cv = texto
        candidato.email = email
        candidato.telefone = telefone
        candidato.resumo = perfil.get("resumo", "")
        candidato.titulo_profissional = perfil.get("titulo_profissional", "")
        candidato.anos_experiencia = perfil.get("anos_experiencia", "")
        candidato.localizacao = perfil.get("localizacao", "")
        candidato.idiomas = perfil.get("idiomas", "")
        candidato.setores = perfil.get("setores", "")

        print(
            "♻️ Talento existente reutilizado:",
            candidato.id,
            "| e-mail:",
            email
        )

    else:

        # Mantém a proteção legada por arquivo + vaga para casos
        # sem identidade segura por e-mail.
        existe_arquivo = (
            db.query(Candidato)
            .filter(
                Candidato.nome_arquivo == arquivo.filename,
                Candidato.vaga_id == vaga.id
            )
            .first()
        )

        if existe_arquivo:
            print(
                f"⚠️ CV já existe: {arquivo.filename}"
            )
            return None

        candidato = Candidato(

            nome_arquivo=arquivo.filename,
            caminho_cv=caminho_cv,
            texto_cv=texto,
            email=email,
            telefone=telefone,
            score=score,
            resumo=perfil.get("resumo", ""),
            titulo_profissional=perfil.get("titulo_profissional", ""),
            anos_experiencia=perfil.get("anos_experiencia", ""),
            localizacao=perfil.get("localizacao", ""),
            idiomas=perfil.get("idiomas", ""),
            setores=perfil.get("setores", ""),
            skills_extraidas=", ".join(
                resultado_match.get("encontradas", [])
            ) if isinstance(resultado_match, dict) else "",
            skills_faltantes=", ".join(
                resultado_match.get("faltantes", [])
            ) if isinstance(resultado_match, dict) else "",
            dados_ia=None,
            vaga_id=vaga.id,
            origem=origem
        )

        db.add(candidato)
        db.flush()

    print(
        "✅ Candidato criado:",
        candidato.nome_arquivo
    )

    # =====================================================
    # CANDIDATURA — TALENT BANK 2.0
    # =====================================================
    #
    # A candidatura representa a relação:
    #
    # TALENTO × VAGA
    #
    # Durante a fase de transição, Candidato continua
    # preservando os campos legados usados pelas telas
    # atuais.
    #
    # O resultado específico da vaga também passa a ser
    # persistido em Candidatura.
    # =====================================================

    candidatura = Candidatura(

        candidato_id=candidato.id,

        vaga_id=vaga.id,

        origem=origem,

        status=candidato.etapa,

        match_score=int(score)
        if score is not None
        else None,

        match_data=None

    )

    db.add(candidatura)

    db.flush()

    print(
        "✅ Candidatura criada:",
        candidatura.id,
        "| candidato:",
        candidato.id,
        "| vaga:",
        vaga.id
    )

    # =========================
    # TALIA
    # =========================

    print()

    print(
        "🚀 Enviando candidato para TALIA..."
    )

    from app.intelligence.context.analysis_context import (
        AnalysisContext
    )

    context = AnalysisContext(

        texto_cv=texto,

        perfil=perfil,

        match=resultado_match,

        historico_profissional=historico_profissional

    )

    print()
    print("========== AUDITORIA SAP MM ==========")

    for nome_fonte, fonte in [
        ("PERFIL", perfil),
        ("HISTORICO", historico_profissional),
        ("TEXTO_CV", getattr(context, "texto_cv", "")),
    ]:
        fonte_str = str(fonte).lower()

        print(
            nome_fonte,
            "| sap mm:",
            "sap mm" in fonte_str,
            "| materials management:",
            "materials management" in fonte_str
        )

    print("======================================")
    print()

    analise_talia = talia.analisar_candidato(

        candidato=candidato,

        vaga=vaga,

        context=context

    )

    # =====================================================
    # TALIA — DECISION OFICIAL
    # =====================================================

    analysis_result = analise_talia.get(
        "decision"
    )

    decision = None

    if isinstance(
        analysis_result,
        dict
    ):

        decision = analysis_result.get(
            "decision"
        )

    else:

        decision = analysis_result


    # =====================================================
    # TALIA — RESULTADO OFICIAL
    # =====================================================

    if decision is not None:

        # =================================================
        # SCORE OFICIAL
        # =================================================

        overall_match = getattr(
            decision,
            "overall_match",
            None
        )

        if overall_match is not None:

            candidato.score = float(
                overall_match
            )

            print(
                "🎯 TALIA Overall Match:",
                candidato.score
            )

        # =================================================
        # MATCH RESULT OFICIAL
        # =================================================

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

            # =============================================
            # FLATTEN TECHNICAL REQUIREMENTS
            # =============================================

            skills_encontradas = []

            skills_faltantes = []

            # =============================================
            # SKILLS ENCONTRADAS
            # =============================================
            #
            # Preserva evidências encontradas em todas
            # as categorias, inclusive diferenciais.

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

            # =============================================
            # SKILLS FALTANTES
            # =============================================
            #
            # Apenas requisitos que representam ausência
            # relevante para a aderência principal.
            #
            # Nice-to-have NÃO é gap obrigatório.

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

            # =============================================
            # REMOVE DUPLICAÇÕES PRESERVANDO A ORDEM
            # =============================================

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

            # =============================================
            # PERSISTÊNCIA DAS SKILLS OFICIAIS TALIA
            # =============================================

            candidato.skills_extraidas = ", ".join(
                skills_encontradas
            )

            candidato.skills_faltantes = ", ".join(
                skills_faltantes
            )

            print(
                "✅ TALIA Skills encontradas:",
                skills_encontradas
            )

            print(
                "⚠️ TALIA Skills sem evidência:",
                skills_faltantes
            )

        else:

            print(
                "⚠️ TALIA MatchResult oficial não encontrado."
            )

    else:

        print(
            "⚠️ TALIA Decision oficial não encontrada."
        )
   

    # =========================
    # RELATÓRIO IA
    # =========================

    relatorio_ia = {

        "perfil": perfil,

        "match": resultado_match,

        "talia": analise_talia

    }

    # =====================================================
    # PERSISTÊNCIA DO RELATÓRIO
    # =====================================================

    candidato.dados_ia = json.dumps(

        relatorio_ia,

        ensure_ascii=False,

        default=_serializar_para_json

    )

    # =====================================================
    # PERSISTÊNCIA DA CANDIDATURA
    # =====================================================
    #
    # A Candidatura recebe o resultado específico desta
    # relação candidato × vaga.
    #
    # Candidato continua recebendo os mesmos dados durante
    # a fase de compatibilidade com as telas legadas.
    # =====================================================

    if candidato.score is not None:

        candidatura.match_score = int(
            round(
                float(
                    candidato.score
                )
            )
        )

    else:

        candidatura.match_score = None

    candidatura.match_data = candidato.dados_ia

    candidatura.status = candidato.etapa

    candidatura.origem = origem

    print(
        "✅ Candidatura atualizada com TALIA:",
        candidatura.id,
        "| match:",
        candidatura.match_score
    )

    # =========================
    # SALVAR
    # =========================

    db.commit()

    db.refresh(candidato)

    db.refresh(candidatura)

    print()

    print(
        "🤖 TALIA respondeu"
    )

    print("=" * 60)

    from pprint import pprint

    pprint(
        analise_talia
    )

    print("=" * 60)

    print()

    return candidato
