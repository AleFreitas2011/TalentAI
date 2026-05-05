from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


# =========================
# 👤 USUARIO
# =========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

    vagas = relationship("Vaga", back_populates="usuario")


# =========================
# 💼 VAGA
# =========================
class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)

    # 🔥 RELAÇÃO CORRETA
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente")

    descricao = Column(Text)
    palavras_chave = Column(Text)

    status = Column(String, default="Aberta")
    data_criacao = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    candidatos_mapeados = Column(Integer, default=0)
    candidatos_entrevistados = Column(Integer, default=0)
    candidatos_enviados = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="vagas")
    candidatos = relationship("Candidato", back_populates="vaga")


# =========================
# 👨‍💼 CANDIDATO
# =========================
class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String)

    email = Column(String)
    telefone = Column(String, nullable=True)

    texto_cv = Column(Text)
    skills_extraidas = Column(Text)
    skills_faltantes = Column(Text)

    score = Column(Float)
    resumo = Column(Text)

    # 🔥 BASE IA
    dados_ia = Column(Text, nullable=True)

    etapa = Column(String, default="Mapeado")

    # 💰 TAXAS
    taxa_candidato = Column(String)
    taxa_cliente = Column(String)

    data_upload = Column(DateTime, default=datetime.utcnow)

    # 🌍 NOVO CAMPO (NOSSO FOCO)
    origem = Column(String, default="Banco Interno")

    vaga_id = Column(Integer, ForeignKey("vagas.id"))
    vaga = relationship("Vaga", back_populates="candidatos")

    idioma = Column(String, default="PT")


# =========================
# 🏢 CLIENTE
# =========================
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_contato = Column(String)
    email = Column(String)
    empresa = Column(String)


# =========================
# 📤 ENVIO (HISTÓRICO)
# =========================
class Envio(Base):
    __tablename__ = "envios"

    id = Column(Integer, primary_key=True, index=True)

    vaga_id = Column(Integer, ForeignKey("vagas.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente")

    data_envio = Column(DateTime, default=datetime.utcnow)

    candidatos = Column(Text)
