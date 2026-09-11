from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from .db import Base


# =====================================================
# USUÁRIOS
# =====================================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)

    senha = Column(String)

    vagas = relationship(
        "Vaga",
        back_populates="usuario"
    )


# =====================================================
# CLIENTES
# =====================================================

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)

    nome_contato = Column(String)

    email = Column(String)

    empresa = Column(String)


# =====================================================
# VAGAS
# =====================================================

class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String)

    descricao = Column(Text)

    palavras_chave = Column(Text)

    status = Column(
        String,
        default="Aberta"
    )

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )

    candidatos_mapeados = Column(
        Integer,
        default=0
    )

    candidatos_entrevistados = Column(
        Integer,
        default=0
    )

    candidatos_enviados = Column(
        Integer,
        default=0
    )

    cliente = relationship("Cliente")

    usuario = relationship(
        "Usuario",
        back_populates="vagas"
    )

    # -------------------------------------------------
    # RELACIONAMENTO LEGADO
    # -------------------------------------------------
    # Mantido durante a transição para o Talent Bank 2.0.
    # Não remover enquanto as rotas atuais ainda utilizarem
    # Candidato.vaga_id.
    candidatos = relationship(
        "Candidato",
        back_populates="vaga"
    )

    # -------------------------------------------------
    # TALENT BANK 2.0
    # -------------------------------------------------
    # Uma vaga pode possuir várias candidaturas.
    candidaturas = relationship(
        "Candidatura",
        back_populates="vaga"
    )


# =====================================================
# CANDIDATOS / TALENTOS
# =====================================================

class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)

    nome_arquivo = Column(String)

    caminho_cv = Column(
        String,
        nullable=True
    )

    texto_cv = Column(Text)

    email = Column(String)

    telefone = Column(
        String,
        nullable=True
    )

    idioma = Column(
        String,
        default="PT"
    )

    origem = Column(
        String,
        default="Banco Interno"
    )

    data_upload = Column(
        DateTime,
        default=datetime.utcnow
    )

    # -------------------------------------------------
    # RELACIONAMENTO LEGADO COM VAGA
    # -------------------------------------------------
    # Mantido temporariamente para preservar todas as
    # funcionalidades atuais durante a migração.
    vaga_id = Column(
        Integer,
        ForeignKey("vagas.id")
    )

    vaga = relationship(
        "Vaga",
        back_populates="candidatos"
    )

    # ======================================
    # SCORE IA
    # ======================================

    # Estes campos permanecem nesta fase por
    # compatibilidade com o sistema atual.
    # O match específico Talent x Vaga passará
    # progressivamente para Candidatura.
    score = Column(Float)

    resumo = Column(Text)

    skills_extraidas = Column(Text)

    skills_faltantes = Column(Text)

    dados_ia = Column(
        Text,
        nullable=True
    )

    # ======================================
    # PERFIL EXECUTIVO IA
    # ======================================

    titulo_profissional = Column(
        String,
        nullable=True
    )

    anos_experiencia = Column(
        String,
        nullable=True
    )

    localizacao = Column(
        String,
        nullable=True
    )

    idiomas = Column(
        String,
        nullable=True
    )

    setores = Column(
        Text,
        nullable=True
    )

    # ======================================
    # DADOS DO RECRUTADOR
    # ======================================

    observacoes_recrutador = Column(
        Text,
        nullable=True
    )

    status_recrutador = Column(
        String,
        default="Novo"
    )

    nivel_ingles = Column(
        String,
        nullable=True
    )

    nivel_espanhol = Column(
        String,
        nullable=True
    )

    disponibilidade = Column(
        String,
        nullable=True
    )

    data_disponibilidade = Column(
        DateTime,
        nullable=True
    )

    modelo_contratacao = Column(
        String,
        nullable=True
    )

    modelo_trabalho = Column(
        String,
        nullable=True
    )

    cliente_atual = Column(
        String,
        nullable=True
    )

    projeto_atual = Column(
        String,
        nullable=True
    )

    interesse_oportunidades = Column(
        Boolean,
        default=True
    )

    ultimo_contato = Column(
        DateTime,
        nullable=True
    )

    proximo_followup = Column(
        DateTime,
        nullable=True
    )

    # ======================================
    # COMERCIAL
    # ======================================

    taxa_candidato = Column(
        String,
        nullable=True
    )

    taxa_cliente = Column(
        String,
        nullable=True
    )

    # ======================================
    # PIPELINE LEGADO
    # ======================================

    etapa = Column(
        String,
        default="Mapeado"
    )

    # ======================================
    # ANOTAÇÕES
    # ======================================

    anotacoes = relationship(
        "AnotacaoRecrutador",
        back_populates="candidato",
        cascade="all, delete-orphan",
        order_by="AnotacaoRecrutador.data_criacao.desc()"
    )

    # ======================================
    # TALENT BANK 2.0
    # ======================================

    # Um talento pode participar de várias vagas
    # sem precisar ser duplicado na base.
    candidaturas = relationship(
        "Candidatura",
        back_populates="candidato"
    )


# =====================================================
# CANDIDATURAS — TALENT BANK 2.0
# =====================================================

class Candidatura(Base):
    __tablename__ = "candidaturas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidato_id = Column(
        Integer,
        ForeignKey("candidatos.id"),
        nullable=False
    )

    vaga_id = Column(
        Integer,
        ForeignKey("vagas.id"),
        nullable=False
    )

    origem = Column(
        String(100),
        nullable=True
    )

    status = Column(
        String(50),
        nullable=True
    )

    # ======================================
    # MATCH TALENTO x VAGA
    # ======================================

    match_score = Column(
        Integer,
        nullable=True
    )

    match_data = Column(
        Text,
        nullable=True
    )

    # ======================================
    # DATAS
    # ======================================

    data_candidatura = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    data_atualizacao = Column(
        DateTime,
        nullable=True
    )

    # ======================================
    # RELACIONAMENTOS
    # ======================================

    candidato = relationship(
        "Candidato",
        back_populates="candidaturas"
    )

    vaga = relationship(
        "Vaga",
        back_populates="candidaturas"
    )


# =====================================================
# ANOTAÇÕES DO RECRUTADOR
# =====================================================

class AnotacaoRecrutador(Base):
    __tablename__ = "anotacoes_recrutador"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidato_id = Column(
        Integer,
        ForeignKey("candidatos.id"),
        nullable=False
    )

    vaga_id = Column(
        Integer,
        ForeignKey("vagas.id"),
        nullable=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=True
    )

    tipo = Column(
        String,
        default="Observação"
    )

    texto = Column(
        Text,
        nullable=False
    )

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidato = relationship(
        "Candidato",
        back_populates="anotacoes"
    )

    vaga = relationship("Vaga")

    usuario = relationship("Usuario")


# =====================================================
# HISTÓRICO DE ENVIOS
# =====================================================

class Envio(Base):
    __tablename__ = "envios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vaga_id = Column(
        Integer,
        ForeignKey("vagas.id")
    )

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    cliente = relationship("Cliente")

    data_envio = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidatos = Column(Text)