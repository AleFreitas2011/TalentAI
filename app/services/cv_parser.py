from pathlib import Path
import pdfplumber
from PyPDF2 import PdfReader
from docx import Document
import re


def extrair_texto_pdf(caminho_arquivo: str) -> str:

    texto = ""

    # =========================
    # TENTATIVA 1 — PDFPLUMBER
    # =========================
    try:

        with pdfplumber.open(caminho_arquivo) as pdf:

            for pagina in pdf.pages:

                conteudo = pagina.extract_text()

                if conteudo:
                    texto += conteudo + "\n"

        if texto.strip():

            print("✅ TEXTO EXTRAÍDO COM PDFPLUMBER")
            print("📄 TEXTO:", texto[:500])

            return texto.strip()

        print("⚠️ PDFPLUMBER não encontrou texto")

    except Exception as e:

        print("🔥 ERRO PDFPLUMBER:", e)

    # =========================
    # TENTATIVA 2 — PYPDF2
    # =========================
    try:

        texto = ""

        reader = PdfReader(caminho_arquivo)

        for pagina in reader.pages:

            conteudo = pagina.extract_text()

            if conteudo:
                texto += conteudo + "\n"

        if texto.strip():

            print("✅ TEXTO EXTRAÍDO COM PYPDF2")
            print("📄 TEXTO:", texto[:500])

            return texto.strip()

        print("⚠️ PYPDF2 também não encontrou texto")

    except Exception as e:

        print("🔥 ERRO PYPDF2:", e)

    # =========================
    # FALHA FINAL
    # =========================
    print("❌ CV NÃO LEGÍVEL")

    return "CV não legível"


def extrair_texto_docx(caminho_arquivo: str) -> str:
    try:
        doc = Document(caminho_arquivo)
        textos = [p.text for p in doc.paragraphs if p.text.strip()]

        texto_final = "\n".join(textos)

        print("📄 DOCX TEXTO:", texto_final[:500])  # DEBUG

        if not texto_final.strip():
            return "CV não legível"

        return texto_final

    except Exception as e:
        print("🔥 ERRO DOCX:", e)
        return "CV não legível"


def extrair_texto_cv(caminho_arquivo: str) -> str:
    extensao = Path(caminho_arquivo).suffix.lower()

    if extensao == ".pdf":
        return extrair_texto_pdf(caminho_arquivo)

    elif extensao == ".docx":
        return extrair_texto_docx(caminho_arquivo)

    elif extensao == ".doc":
        return "Formato .doc não suportado"

    else:
        return "Formato não suportado"
    
 